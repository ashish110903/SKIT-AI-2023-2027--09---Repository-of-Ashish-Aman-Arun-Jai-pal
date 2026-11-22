class AlertDispatcher:
    def broadcast(self, severity: str, msg: str):
        print(f'[ALERT BROADCAST] {severity}: {msg}')

alert_dispatcher = AlertDispatcher()
