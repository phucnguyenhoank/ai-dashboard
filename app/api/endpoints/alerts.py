from fastapi import APIRouter, Query
from datetime import datetime
from pydantic import BaseModel
from app.core.database import detections_collection
from app.schemas.alert import AlertTypePercentage, AlertStatistics

router = APIRouter(prefix="/ai", tags=["alerts"])


@router.get("/alerts/statistics", response_model=AlertStatistics)
async def get_alert_statistics(
    start_time: datetime = Query(None, description="Filter alerts after this timestamp"),
    end_time: datetime = Query(None, description="Filter alerts before this timestamp")
):

    # Build the aggregation pipeline
    pipeline = []
    
    # Add optional time range filter
    if start_time or end_time:
        match_stage = {"timestamp": {}}
        if start_time:
            match_stage["timestamp"]["$gte"] = start_time
        if end_time:
            match_stage["timestamp"]["$lte"] = end_time
        pipeline.append({"$match": match_stage})
    
    # Facet stage to compute all statistics in one query
    pipeline.append({
        "$facet": {
            "total": [{"$count": "count"}],
            "unread": [{"$match": {"seen": False}}, {"$count": "count"}],
            "read": [{"$match": {"seen": True}}, {"$count": "count"}],
            "types": [{"$group": {"_id": "$type", "count": {"$sum": 1}}}]
        }
    })
    
    # Execute the aggregation and get the result
    result = list(detections_collection.aggregate(pipeline))[0]
    
    # Extract counts, defaulting to 0 if no data
    total_alerts = result["total"][0]["count"] if result["total"] else 0
    unread_alerts = result["unread"][0]["count"] if result["unread"] else 0
    read_alerts = result["read"][0]["count"] if result["read"] else 0
    types = result["types"]
    
    # Calculate percentages for each alert type
    total_alert_percentages = [
        AlertTypePercentage(
            type=t["_id"],
            count=t["count"],
            percentage=round((t["count"] / total_alerts * 100) if total_alerts > 0 else 0, 1)
        )
        for t in types
    ]
    
    # Construct and return the response
    return AlertStatistics(
        total_alerts=total_alerts,
        unread_alerts=unread_alerts,
        read_alerts=read_alerts,
        total_alert_percentages=total_alert_percentages
    )