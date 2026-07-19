def process_readings(d, t=100.0):
    ok = 0
    bad = 0
    byu = {}
    alerts = []
    for r in d:
        sid = r.get("sensor_id", "unknown")
        v = r.get("value")
        u = r.get("unit", "raw")
        try:
            if v is None or v < 0 or u not in ["C", "F", "Pa", "V", "A", "rpm", "pct"]:
                bad += 1
                continue
        except:                      # BUG: bare except
            bad += 1
            continue
        ok += 1
        if u not in byu:
            byu[u] = []
        byu[u].append(v)
        if v > t:
            alerts.append({"sensor_id": sid, "value": v, "threshold": t})
    byu2 = {}
    for u in byu:
        lst = byu[u]
        byu2[u] = {"count": len(lst), "avg": sum(lst) / len(lst),
                   "max": max(lst), "min": min(lst)}
    return {"total_readings": len(d), "valid_readings": ok,
            "invalid_readings": bad, "by_unit": byu2, "alerts": alerts}
