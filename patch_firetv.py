from pathlib import Path
p = Path("app/src/main/java/com/example/alek/ble_hid_example/HidBleService.java")
s = p.read_text(encoding="utf-8")
old = """        AdvertiseData scanResponse = new AdvertiseData.Builder()
                .addServiceUuid(new ParcelUuid(UUID.fromString(SERVICE_DIS)))
                .addServiceUuid(new ParcelUuid(UUID.fromString(SERVICE_BAS)))
                .build();"""
new = """        // Experimental Amazon manufacturer data. NOT verified as a Fire TV remote advertisement.
        // Manufacturer ID 0x0171 is encoded by Android in little-endian.
        // Product 0x041C is a test hypothesis, not a captured advertising payload.
        AdvertiseData scanResponse = new AdvertiseData.Builder()
                .addServiceUuid(new ParcelUuid(UUID.fromString(SERVICE_DIS)))
                .addServiceUuid(new ParcelUuid(UUID.fromString(SERVICE_BAS)))
                .addManufacturerData(0x0171, new byte[] {(byte) 0x1C, (byte) 0x04})
                .build();"""
if s.count(old) != 1:
    raise SystemExit("Source changed: expected advertising block not found exactly once")
s = s.replace(old, new)
# Make BLE advertising success/failure visible on the phone.
success = '            Log.i("BLE", "Advertisement started successfully");'
failure = '            Log.i("BLE", "Advertisement not started - error: " + errorCode);'
if s.count(success) != 1 or s.count(failure) != 1:
    raise SystemExit("Advertising callbacks changed")
s = s.replace(success, success + '\\n            new Handler(Looper.getMainLooper()).post(() -> Toast.makeText(getApplicationContext(), "BLE advertising ACTIVE", Toast.LENGTH_LONG).show());')
s = s.replace(failure, failure + '\\n            new Handler(Looper.getMainLooper()).post(() -> Toast.makeText(getApplicationContext(), "BLE advertising FAILED: " + errorCode, Toast.LENGTH_LONG).show());')
# Explicitly report when advertising cannot start before the callback.
notready = '            Log.d("BLE", "GATT Database not fully registered yet, postponing startAdvertising()");'
if s.count(notready) != 1:
    raise SystemExit("GATT readiness check changed")
s = s.replace(notready, notready + '\\n            new Handler(Looper.getMainLooper()).post(() -> Toast.makeText(getApplicationContext(), "BLE waiting for GATT initialization", Toast.LENGTH_LONG).show());')
p.write_text(s, encoding="utf-8")
print("Patched:",p)
