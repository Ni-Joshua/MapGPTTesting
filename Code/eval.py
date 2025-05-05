import math
import pandas as pd
import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance between two points on the Earth (in kilometers).
    Uses the Haversine formula.
    """
    R = 6371.0  # Earth's radius in kilometers
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def evaluate_bbox_prediction(bbox_gt, bbox_pred):
    """
    Evaluate the accuracy of a predicted bounding box against the ground truth.
    Designed for historical map localization tasks using geographic coordinates.

    Args:
        bbox_gt: tuple (lon_min, lon_max, lat_max, lat_min) - Ground truth bounding box
        bbox_pred: tuple (lon_min, lon_max, lat_max, lat_min) - Predicted bounding box

    Returns:
        Dictionary of evaluation metrics:
            - IoU: Intersection over Union
            - Area Similarity: Ratio of smaller to larger area
            - Center Shift (km): Haversine distance between centers
            - GT in Pred: Whether GT box is fully within predicted box
            - Pred in GT: Whether predicted box is fully within GT box
    """
    lon_min_gt, lon_max_gt, lat_max_gt, lat_min_gt = bbox_gt
    lon_min_pred, lon_max_pred, lat_max_pred, lat_min_pred = bbox_pred

    # Compute areas
    gt_area = (lon_max_gt - lon_min_gt) * (lat_max_gt - lat_min_gt)
    pred_area = (lon_max_pred - lon_min_pred) * (lat_max_pred - lat_min_pred)

    # Compute intersection bbox
    inter_lon_min = max(lon_min_gt, lon_min_pred)
    inter_lon_max = min(lon_max_gt, lon_max_pred)
    inter_lat_min = max(lat_min_gt, lat_min_pred)
    inter_lat_max = min(lat_max_gt, lat_max_pred)

    if inter_lon_min >= inter_lon_max or inter_lat_min >= inter_lat_max:
        inter_area = 0.0
    else:
        inter_area = (inter_lon_max - inter_lon_min) * (inter_lat_max - inter_lat_min)

    # IoU calculation
    union_area = gt_area + pred_area - inter_area
    iou = inter_area / union_area if union_area > 0 else 0.0

    # Area similarity (symmetric ratio)
    area_similarity = min(gt_area, pred_area) / max(gt_area, pred_area) if max(gt_area, pred_area) > 0 else 0.0

    # Compute center points
    center_lon_gt = (lon_min_gt + lon_max_gt) / 2
    center_lat_gt = (lat_min_gt + lat_max_gt) / 2
    center_lon_pred = (lon_min_pred + lon_max_pred) / 2
    center_lat_pred = (lat_min_pred + lat_max_pred) / 2

    # Center distance using haversine formula
    center_shift_km = haversine_distance(center_lat_gt, center_lon_gt, center_lat_pred, center_lon_pred)

    # Containment checks
    pred_in_gt = (
        lon_min_pred >= lon_min_gt and lon_max_pred <= lon_max_gt and
        lat_min_pred >= lat_min_gt and lat_max_pred <= lat_max_gt
    )

    gt_in_pred = (
        lon_min_gt >= lon_min_pred and lon_max_gt <= lon_max_pred and
        lat_min_gt >= lat_min_pred and lat_max_gt <= lat_max_pred
    )

    return {
        "IoU": round(iou, 4),
        "Area Similarity": round(area_similarity, 4),
        "Center Shift (km)": round(center_shift_km, 2),
        "GT in Pred": gt_in_pred,
        "Pred in GT": pred_in_gt
    }

def computeAll(GT, ModelPred, Testname):
    print(Testname)
    avgIOU = 0
    avgArea = 0
    avgShift = 0
    gtinPredCount = 0
    predinGTCount = 0
    for i in range(0, len(GT)):
        x = evaluate_bbox_prediction(GT[i],ModelPred[i])
        avgIOU+=x["IoU"]
        avgArea+=x["Area Similarity"]
        avgShift+=x['Center Shift (km)']
        if (x["GT in Pred"]):
            gtinPredCount+=1
        if (x['Pred in GT']):
            predinGTCount+=1
        # print(x)
    avgIOU = avgIOU/len(GT)
    avgArea = avgArea/len(GT)
    avgShift = avgShift/len(GT)
    print("Overall Summary")
    print(f"Average IoU: {avgIOU}")
    print(f"Average Area Similarity: {avgArea}")
    print(f"Average Center Shift (km): {avgShift}")
    print(f"Total Number of GT in Pred: {gtinPredCount}")
    print(f"Total Number of Pred in GT: {predinGTCount}")

def computeFromDF(df):
    GT = df['Ground Truth'].values
    ModelPred = df['Response'].values
    i=0
    while(i < len(GT)):
        if("(" not in ModelPred[i]):
            GT = np.delete(GT, i, axis=0)
            ModelPred = np.delete(ModelPred, i, axis = 0)
        else:
            ModelPred[i] = np.array(ModelPred[i].split("(")[1].split(")")[0].split(', '), dtype=float)
            GT[i] = np.array(GT[i].split("(")[1].split(")")[0].split(','), dtype=float)
            i+=1
    computeAll(GT, ModelPred, "4o")

if __name__ == "__main__":
    df = pd.read_csv("Map2Loc_GPTResults/4oTestResults3_Completed.csv")
    computeFromDF(df)
    df = pd.read_csv("Map2Loc_GPTResults/4oTestResults4_Completed.csv")
    computeFromDF(df)
    df = pd.read_csv("Map2Loc_GPTResults/4oTestResults5_Completed.csv")
    computeFromDF(df)






