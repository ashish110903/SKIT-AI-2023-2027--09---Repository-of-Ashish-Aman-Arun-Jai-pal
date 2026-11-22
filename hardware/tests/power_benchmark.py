def benchmark_power():
    active_ma = 22.4
    sleep_ua = 18.2
    daily_consumption_mah = (active_ma * (1/60)) + (sleep_ua/1000 * (59/60)) * 24
    battery_days = 3200 / daily_consumption_mah
    print(f'Estimated battery life without solar: {battery_days:.1f} days')
if __name__ == '__main__': benchmark_power()
