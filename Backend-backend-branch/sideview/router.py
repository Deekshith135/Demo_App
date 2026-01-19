# backend/sideview/router.py
"""
Sideview Router - Coconut Tree Disease Detection (Transfer Model)
Provides API endpoints for disease detection in coconut trees using:
- Single image prediction
- Video processing with frame-by-frame analysis
"""

import sys
import os
import json
import shutil
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# ✅ recommendation.py must be in ROOT (same folder as main.py)
from recommendation import get_recommendation

# Setup logging
logger = logging.getLogger(__name__)

# Configure paths
SIDEVIEW_ROOT = Path(__file__).parent
SCRIPTS_DIR = SIDEVIEW_ROOT / "scripts"
UPLOADS_DIR = SIDEVIEW_ROOT / "uploads"
RESULTS_DIR = SIDEVIEW_ROOT / "results"
MODEL_PATH = SIDEVIEW_ROOT / "plant_disease_transfer_model.h5"
LABELS_PATH = SIDEVIEW_ROOT / "labels.json"

# Ensure directories exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Add scripts directory to path for imports
if str(SIDEVIEW_ROOT) not in sys.path:
    sys.path.insert(0, str(SIDEVIEW_ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Import local modules
try:
    from sideview.test_transfer_model import TransferModelPredictor
    from sideview.scripts.video_to_phase2 import run_pipeline
    from sideview.scripts.generate_video_report_v2 import generate_report
    from sideview.scripts.aggregate_dashboard import aggregate_dashboard, VALID_DISEASES_BY_PART
    
    MODULES_AVAILABLE = True
    logger.info("Sideview modules loaded successfully")
except ImportError as e:
    MODULES_AVAILABLE = False
    logger.error(f"Failed to import sideview modules: {e}")
    TransferModelPredictor = None
    run_pipeline = None
    generate_report = None
    aggregate_dashboard = None
    VALID_DISEASES_BY_PART = None

# Create router
router = APIRouter(
    prefix="/sideview",
    tags=["Sideview - Disease Detection"],
    responses={
        500: {"description": "Internal server error"},
        400: {"description": "Bad request"},
    }
)

# Lazy-loaded global predictor for single-image endpoint
_image_predictor: Optional[TransferModelPredictor] = None

# ✅ In-memory storage for last image and last video (for recommendation endpoint)
LAST_IMAGE_PREDICTION: Optional[dict] = None
LAST_VIDEO_DASHBOARD: Optional[dict] = None
LAST_USED: Optional[str] = None  # "image" or "video"


def _get_predictor() -> TransferModelPredictor:
    """Initialize and return the image predictor (singleton pattern)."""
    global _image_predictor
    
    if _image_predictor is None:
        if not MODULES_AVAILABLE or TransferModelPredictor is None:
            raise HTTPException(
                status_code=500,
                detail="Prediction modules not available"
            )
        
        if not MODEL_PATH.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Model not found at {MODEL_PATH}"
            )
        if not LABELS_PATH.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Labels file not found at {LABELS_PATH}"
            )
        
        _image_predictor = TransferModelPredictor(
            model_path=str(MODEL_PATH),
            labels_path=str(LABELS_PATH)
        )
        logger.info("Transfer model loaded successfully")
    
    return _image_predictor


@router.get("/", summary="Sideview API Info")
async def sideview_root():
    """Get information about the Sideview Disease Detection API."""
    return {
        "message": "Coconut Tree Disease Detection API (Sideview)",
        "version": "1.0.0",
        "status": "operational" if MODULES_AVAILABLE else "degraded",
        "endpoints": {
            "predict_image": "/sideview/predict_image",
            "process_video": "/sideview/process_video",
            "recommendation": "/sideview/recommendation"
        },
        "capabilities": {
            "image_prediction": MODULES_AVAILABLE and MODEL_PATH.exists(),
            "video_processing": MODULES_AVAILABLE and MODEL_PATH.exists()
        }
    }


@router.post("/predict_image", summary="Predict Disease from Image")
async def predict_image_endpoint(file: UploadFile = File(...)):
    """
    Predict disease, part, and health status for a single uploaded image.
    Stores last image prediction for recommendation endpoint.
    
    Args:
        file: Image file (JPG, PNG) of coconut tree part
        
    Returns:
        JSON containing:
        - image: Path to uploaded image
        - prediction: Disease classification results with confidence scores
    """
    global LAST_IMAGE_PREDICTION, LAST_USED
    
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image file."
            )
        
        # Get predictor (loads model if needed)
        predictor = _get_predictor()
        
        # Save uploaded image
        image_upload_dir = UPLOADS_DIR / "images"
        image_upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = image_upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Run prediction
        result = predictor.predict(str(file_path))
        
        # ✅ Store for recommendation endpoint
        LAST_IMAGE_PREDICTION = result
        LAST_USED = "image"
        
        logger.info(f"Image prediction completed: {file.filename}")
        
        return {
            "success": True,
            "image": str(file_path),
            "filename": file.filename,
            "prediction": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/process_video", summary="Process Video for Disease Detection")
async def process_video_endpoint(file: UploadFile = File(...)):
    """
    Process video file to detect diseases frame-by-frame.
    Stores last dashboard for recommendation endpoint.
    
    Args:
        file: Video file (MP4, AVI, MOV) of coconut tree
        
    Returns:
        JSON containing:
        - video: Path to uploaded video
        - predictions: Frame-by-frame prediction results
        - dashboard: Aggregated analysis dashboard
        - report_url: URL to HTML report
    """
    global LAST_VIDEO_DASHBOARD, LAST_USED
    
    try:
        # Check module availability
        if not MODULES_AVAILABLE or run_pipeline is None or generate_report is None:
            raise HTTPException(
                status_code=500,
                detail="Video pipeline modules not available"
            )
        
        # Validate file type
        if not file.content_type or not file.content_type.startswith('video/'):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a video file."
            )
        
        # Check model availability
        if not MODEL_PATH.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Model not found at {MODEL_PATH}"
            )
        
        # Save uploaded video
        file_path = UPLOADS_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Processing video: {file.filename}")
        
        # Run the video processing pipeline
        output_json_path = run_pipeline(
            video_path=str(file_path),
            phase2_model=str(MODEL_PATH),
            frame_interval=0,  # Auto-detect interval
            debug=False,
        )
        
        # Generate HTML report
        generate_report(Path(output_json_path))
        
        # Load the result JSON
        with open(output_json_path, "r") as f:
            result_data = json.load(f)

        # Extract and format predictions
        predictions = result_data.get("predictions", [])
        formatted_predictions = _format_predictions(predictions)
        
        # Generate dashboard
        dashboard = aggregate_dashboard(formatted_predictions)
        
        # ✅ Store dashboard for recommendation endpoint
        LAST_VIDEO_DASHBOARD = dashboard
        LAST_USED = "video"
        
        # Get report URL and paths
        json_path_obj = Path(output_json_path)
        timestamp_folder = json_path_obj.parent.name
        result_dir = json_path_obj.parent
        
        # Save dashboard.json
        dashboard_path = result_dir / "dashboard.json"
        with open(dashboard_path, "w") as f:
            json.dump(dashboard, f, indent=2)
        
        logger.info(f"Dashboard saved: {dashboard_path}")
        logger.info(f"Video processing completed: {file.filename}")
        
        return {
            "success": True,
            "video": str(file_path),
            "filename": file.filename,
            "predictions": formatted_predictions,
            "dashboard": dashboard,
            "dashboard_path": str(dashboard_path),
            "report_url": f"/results/{timestamp_folder}/video_report.html",
            "total_frames": len(formatted_predictions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video processing error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Video processing failed: {str(e)}"
        )


def _format_predictions(predictions: list) -> list:
    """
    Format and filter predictions from the video pipeline.
    
    - Normalize part names ('leaf' -> 'leaves')
    - Enforce part-disease compatibility
    - Filter out Unknown predictions
    
    Args:
        predictions: Raw predictions from pipeline
        
    Returns:
        List of formatted prediction dictionaries
    """
    if not VALID_DISEASES_BY_PART:
        return []
    
    formatted_predictions = []
    
    for pred_entry in predictions:
        prediction_detail = pred_entry.get("prediction", {}) or {}
        
        # Extract status
        status_field = prediction_detail.get("status")
        if isinstance(status_field, dict):
            raw_status = status_field.get("prediction")
            status_conf = float(status_field.get("confidence") or 0.0)
        else:
            raw_status = status_field
            status_conf = 0.0
        raw_status = raw_status or "Unknown"
        
        # Extract and normalize part
        part_field = prediction_detail.get("part")
        if isinstance(part_field, dict):
            part = part_field.get("prediction")
            part_conf = float(part_field.get("confidence") or 0.0)
        else:
            part = part_field
            part_conf = 0.0
        
        # Normalize 'leaf' to 'leaves'
        if part == "leaf":
            part = "leaves"
        
        # Enforce part-disease compatibility
        display_status = raw_status
        if part and raw_status not in (None, "Unknown"):
            allowed = VALID_DISEASES_BY_PART.get(part, set())
            if allowed and raw_status not in allowed:
                display_status = "Unknown"
        
        # Skip Unknown statuses
        if display_status == "Unknown" or not part:
            continue
        
        formatted_predictions.append({
            "frame_index": pred_entry.get("frame_index"),
            "class": pred_entry.get("class"),
            "image_path": prediction_detail.get("image_path") or pred_entry.get("file"),
            "part": {
                "prediction": part,
                "confidence": part_conf,
            },
            "status": {
                "prediction": display_status,
                "confidence": status_conf,
            },
            "health": prediction_detail.get("health"),
            "combined": prediction_detail.get("combined"),
            "is_out_of_distribution": prediction_detail.get("is_out_of_distribution", False),
            "ood_reason": prediction_detail.get("ood_reason"),
            "ood_signals": prediction_detail.get("ood_signals"),
            "reliability": prediction_detail.get("reliability", 0),
        })
    
    return formatted_predictions


# ✅ Helper: map dashboard disease names -> recommendation keys
def _map_dashboard_disease_to_label(disease_name: str) -> str:
    """Map dashboard disease names to recommendation.py keys."""
    name_map = {
        "leaf rot": "leaf_rot",
        "grey leaf rot": "leaves_grey_leaf_rot",
        "bud rot": "bud_rot",
        "bud root dropping": "bud_rot_drooping",
        "bud rot dropping": "bud_rot_drooping",
        "stem bleeding": "stem_bleeding",
        "whitefly": "whitefly",
    }
    return name_map.get((disease_name or "").strip().lower(), "healthy")


# ✅ Helper: recommendation for one part using dashboard diseases
def _get_part_recommendation(part_name: str, part_data: dict) -> dict:
    """Generate recommendation for a single part based on dashboard data."""
    diseases = (part_data or {}).get("diseases", {}) or {}

    # ✅ If no diseases, treat as healthy and give PART-specific practices
    if not diseases:
        return {
            "part": part_name,
            "health": "healthy",
            "recommendation": get_recommendation("healthy", 100, part=part_name)
        }

    # Choose top disease by percentage
    disease_name, score = max(diseases.items(), key=lambda x: float(x[1]))
    score = float(score)

    predicted_label = _map_dashboard_disease_to_label(disease_name)

    return {
        "part": part_name,
        "health": "unhealthy",
        "predicted_label": predicted_label,
        "confidence": score,
        "recommendation": get_recommendation(predicted_label, score, part=part_name)
    }


# ✅✅ Recommendation endpoint (works for both Image + Video)
@router.get("/recommendation", summary="Get Recommendation (Last Used: Image or Video)")
async def recommendation_endpoint():
    """
    Returns recommendation based on LAST USED:
    - image -> prediction label + confidence
    - video -> recommendations for stem + leaves + bud at once
    """
    if LAST_USED is None:
        raise HTTPException(
            status_code=400,
            detail="No recent image/video prediction found. Call /predict_image or /process_video first."
        )

    # ✅ IMAGE recommendation
    if LAST_USED == "image":
        if LAST_IMAGE_PREDICTION is None:
            raise HTTPException(status_code=400, detail="No image prediction available.")

        predicted_label = LAST_IMAGE_PREDICTION.get("predicted_label", "")

        if isinstance(LAST_IMAGE_PREDICTION.get("status"), dict):
            confidence = float(LAST_IMAGE_PREDICTION.get("status", {}).get("confidence", 0))
        else:
            confidence = float(LAST_IMAGE_PREDICTION.get("confidence", 0))

        return {
            "source": "image",
            "predicted_label": predicted_label,
            "confidence": confidence,
            "recommendation": get_recommendation(predicted_label, confidence)
        }

    # ✅ VIDEO recommendation (return all 3 parts)
    if LAST_USED == "video":
        if LAST_VIDEO_DASHBOARD is None:
            raise HTTPException(status_code=400, detail="No video dashboard available.")

        parts = LAST_VIDEO_DASHBOARD.get("parts", {}) or {}
        
        stem_rec = _get_part_recommendation("stem", parts.get("stem"))
        leaves_rec = _get_part_recommendation("leaves", parts.get("leaves"))
        bud_rec = _get_part_recommendation("bud", parts.get("bud"))

        return {
            "source": "video",
            "recommendations": {
                "stem": stem_rec,
                "leaves": leaves_rec,
                "bud": bud_rec,
            }
        }

    raise HTTPException(status_code=400, detail="Invalid last used state.")
