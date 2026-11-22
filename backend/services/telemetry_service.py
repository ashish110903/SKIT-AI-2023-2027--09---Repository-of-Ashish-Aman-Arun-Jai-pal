class TelemetryService:
    def __init__(self):
        self.buffer = []
    def record(self, payload: dict):
        self.buffer.append(payload)
        if len(self.buffer) > 50:
            self.flush()
    def flush(self):
        self.buffer.clear()

telemetry_service = TelemetryService()
