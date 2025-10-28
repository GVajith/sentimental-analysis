import pandas as pd
import io
from fastapi.responses import StreamingResponse


def dataframe_to_stream(df: pd.DataFrame, filename: str = "result.csv"):
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="text/csv",
                             headers={"Content-Disposition": f"attachment; filename={filename}"})
