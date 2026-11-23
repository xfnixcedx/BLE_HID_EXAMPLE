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
p.write_text(s.replace(old,new), encoding="utf-8")
print("Patched:",p)
