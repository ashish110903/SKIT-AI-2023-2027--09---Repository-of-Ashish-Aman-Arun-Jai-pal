class SMSNotifier:
    def send_emergency_sms(self, phone: str, text: str):
        print(f'[SMS OUTBOUND] To {phone}: {text}')
sms_notifier = SMSNotifier()
