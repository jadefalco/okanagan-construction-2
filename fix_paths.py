import os
from pathlib import Path

# Find images directory (checks both images/ and public/images/)
base = Path(".")
possible = [base / "images", base / "public" / "images"]
images_dir = next((p for p in possible if p.exists()), None)

if not images_dir:
    print("ERROR: Could not find images/ or public/images/")
    exit(1)

print(f"Found images at: {images_dir}")
print("=" * 50)

def rename_item(old_rel, new_rel):
    """Rename a file or folder, handling Windows case-insensitivity"""
    old_path = images_dir / old_rel
    new_path = images_dir / new_rel
    
    if not old_path.exists():
        print(f"  SKIP: {old_rel} (not found)")
        return
    
    # Windows case-only rename needs a temp step
    if old_rel != new_rel and old_rel.lower() == new_rel.lower():
        temp_rel = old_rel + "-temp"
        temp_path = images_dir / temp_rel
        old_path.rename(temp_path)
        temp_path.rename(new_path)
        print(f"  OK: {old_rel} -> {new_rel} (via temp)")
    else:
        old_path.rename(new_path)
        print(f"  OK: {old_rel} -> {new_rel}")

# === FILES FIRST (under old folder names) ===
print("\n--- Renaming files ---")
rename_item("Lakeside Getaway/Orginal Photos/great room.jpeg", "Lakeside Getaway/Orginal Photos/great-room.jpeg")
rename_item("Lakeside Getaway/Orginal Photos/kitchen 2.jpeg", "Lakeside Getaway/Orginal Photos/kitchen-2.jpeg")
rename_item("Lakeside Getaway/After - prof/Exterior/Draper-exterior-5-crop2.JPG", "Lakeside Getaway/After - prof/Exterior/draper-exterior-5-crop2.jpg")
rename_item("Med Cliffside/Exterior/IMG_0154.JPG", "Med Cliffside/Exterior/img_0154.jpg")
rename_item("Lakeside Getaway/Orginal Photos/FinchOutside2.jpg", "Lakeside Getaway/Orginal Photos/finchoutside2.jpg")
rename_item("Lakeside Getaway/Orginal Photos/Finch1.jpg", "Lakeside Getaway/Orginal Photos/finch1.jpg")

# === FOLDERS DEEPEST FIRST ===
print("\n--- Renaming folders ---")
# Depth 5
rename_item("Lakeside Getaway/After - prof web/Living_Space", "Lakeside Getaway/After - prof web/living_space")
rename_item("Lakeside Getaway/After - prof web/Guest_Room", "Lakeside Getaway/After - prof web/guest_room")
rename_item("Lakeside Getaway/After - prof web/Highlights", "Lakeside Getaway/After - prof web/highlights")
rename_item("Lakeside Getaway/After - prof web/Exterior", "Lakeside Getaway/After - prof web/exterior")
rename_item("Lakeside Getaway/After - prof web/Kitchen", "Lakeside Getaway/After - prof web/kitchen")
rename_item("Lakeside Getaway/After - prof/Living_Space", "Lakeside Getaway/After - prof/living_space")
rename_item("Lakeside Getaway/After - prof/Guest_Room", "Lakeside Getaway/After - prof/guest_room")
rename_item("Lakeside Getaway/After - prof/Exterior", "Lakeside Getaway/After - prof/exterior")
rename_item("Med Cliffside/Exterior", "Med Cliffside/exterior")
rename_item("Med Cliffside/Interior", "Med Cliffside/interior")

# Depth 4
rename_item("Lakeside Getaway/After - prof web", "Lakeside Getaway/after-prof-web")
rename_item("Lakeside Getaway/After - prof", "Lakeside Getaway/after-prof")
rename_item("Lakeside Getaway/Orginal Photos", "Lakeside Getaway/orginal-photos")

# Depth 3
rename_item("Lakeside Getaway", "lakeside-getaway")
rename_item("Med Cliffside", "med-cliffside")

# === CODE REPLACEMENTS ===
print("\n--- Updating code files ---")

replacements = [
    ("../images/Lakeside Getaway/After - prof web/Highlights/Draper-masterbedroom-12.jpg", "../images/lakeside-getaway/after-prof-web/highlights/draper-masterbedroom-12.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Living_Space/Draper-livingroom-13.jpg", "../images/lakeside-getaway/after-prof-web/living_space/draper-livingroom-13.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Living_Space/Draper-livingroom-14.jpg", "../images/lakeside-getaway/after-prof-web/living_space/draper-livingroom-14.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Living_Space/Draper-livingroom-6.jpg", "../images/lakeside-getaway/after-prof-web/living_space/draper-livingroom-6.jpg"),
    ("images/Lakeside Getaway/After - prof web/Living_Space/Draper-livingroom-7.jpg", "images/lakeside-getaway/after-prof-web/living_space/draper-livingroom-7.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Guest_Room/Draper-guestbath-2.jpg", "../images/lakeside-getaway/after-prof-web/guest_room/draper-guestbath-2.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Highlights/Draper-guestbath-5.jpg", "../images/lakeside-getaway/after-prof-web/highlights/draper-guestbath-5.jpg"),
    ("../images/Lakeside Getaway/After - prof/Exterior/Draper-exterior-5-crop2.JPG", "../images/lakeside-getaway/after-prof/exterior/draper-exterior-5-crop2.jpg"),
    ("../images/Lakeside Getaway/After - prof/Living_Space/Draper-livingroom-3.jpg", "../images/lakeside-getaway/after-prof/living_space/draper-livingroom-3.jpg"),
    ("images/Lakeside Getaway/After - prof web/Highlights/Draper-livingroom-6.jpg", "images/lakeside-getaway/after-prof-web/highlights/draper-livingroom-6.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Exterior/Draper-exterior-5.jpg", "../images/lakeside-getaway/after-prof-web/exterior/draper-exterior-5.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Exterior/Draper-exterior-2.jpg", "../images/lakeside-getaway/after-prof-web/exterior/draper-exterior-2.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Exterior/Draper-exterior-1.jpg", "../images/lakeside-getaway/after-prof-web/exterior/draper-exterior-1.jpg"),
    ("../images/Med Cliffside/Exterior/1231089_600424323342831_1242145905_n.jpg", "../images/med-cliffside/exterior/1231089_600424323342831_1242145905_n.jpg"),
    ("../images/Med Cliffside/Interior/1009930_600423936676203_1508538106_n.jpg", "../images/med-cliffside/interior/1009930_600423936676203_1508538106_n.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Kitchen/Draper-kitchen-2.jpg", "../images/lakeside-getaway/after-prof-web/kitchen/draper-kitchen-2.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Kitchen/Draper-kitchen-9.jpg", "../images/lakeside-getaway/after-prof-web/kitchen/draper-kitchen-9.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Kitchen/Draper-kitchen-5.jpg", "../images/lakeside-getaway/after-prof-web/kitchen/draper-kitchen-5.jpg"),
    ("../images/Lakeside Getaway/After - prof web/Kitchen/Draper-kitchen-7.jpg", "../images/lakeside-getaway/after-prof-web/kitchen/draper-kitchen-7.jpg"),
    ("../images/Med Cliffside/Interior/578474_600424783342785_1476461897_n.jpg", "../images/med-cliffside/interior/578474_600424783342785_1476461897_n.jpg"),
    ("../images/Med Cliffside/Interior/996824_600424070009523_1224111733_n.jpg", "../images/med-cliffside/interior/996824_600424070009523_1224111733_n.jpg"),
    ("images/Lakeside Getaway/After - prof web/Exterior/Draper-exterior-5.jpg", "images/lakeside-getaway/after-prof-web/exterior/draper-exterior-5.jpg"),
    ("../images/Med Cliffside/Exterior/565038_600424443342819_831062533_n.jpg", "../images/med-cliffside/exterior/565038_600424443342819_831062533_n.jpg"),
    ("../images/Med Cliffside/Interior/76820_600423746676222_1162567912_n.jpg", "../images/med-cliffside/interior/76820_600423746676222_1162567912_n.jpg"),
    ("../images/Lakeside Getaway/After - prof/Guest_Room/bunkbed.jpg", "../images/lakeside-getaway/after-prof/guest_room/bunkbed.jpg"),
    ("../images/Lakeside Getaway/Orginal Photos/FinchOutside2.jpg", "../images/lakeside-getaway/orginal-photos/finchoutside2.jpg"),
    ("../images/Lakeside Getaway/Orginal Photos/great room.jpeg", "../images/lakeside-getaway/orginal-photos/great-room.jpeg"),
    ("../images/Lakeside Getaway/Orginal Photos/kitchen 2.jpeg", "../images/lakeside-getaway/orginal-photos/kitchen-2.jpeg"),
    ("../images/Med Cliffside/Exterior/20140505_131025.jpeg", "../images/med-cliffside/exterior/20140505_131025.jpeg"),
    ("../images/Med Cliffside/Exterior/20140501_195428.jpeg", "../images/med-cliffside/exterior/20140501_195428.jpeg"),
    ("../images/Med Cliffside/Exterior/20140430_202853.jpg", "../images/med-cliffside/exterior/20140430_202853.jpg"),
    ("images/Med Cliffside/Exterior/20140505_131025.jpeg", "images/med-cliffside/exterior/20140505_131025.jpeg"),
    ("images/Lakeside Getaway/Orginal Photos/Finch1.jpg", "images/lakeside-getaway/orginal-photos/finch1.jpg"),
    ("../images/Med Cliffside/Interior/show3993445.png", "../images/med-cliffside/interior/show3993445.png"),
    ("../images/Med Cliffside/Interior/show3993469.jpg", "../images/med-cliffside/interior/show3993469.jpg"),
    ("../images/Med Cliffside/Interior/show3993447.jpg", "../images/med-cliffside/interior/show3993447.jpg"),
    ("../images/Med Cliffside/Interior/show3993459.jpg", "../images/med-cliffside/interior/show3993459.jpg"),
    ("../images/Med Cliffside/Interior/show3993460.jpg", "../images/med-cliffside/interior/show3993460.jpg"),
    ("images/Med Cliffside/Exterior/show3993446.jpg", "images/med-cliffside/exterior/show3993446.jpg"),
    ("../images/Med Cliffside/Exterior/IMG_0154.JPG", "../images/med-cliffside/exterior/img_0154.jpg"),
]

exts = ('.html', '.css', '.js', '.tsx', '.jsx', '.ts', '.mdx')
updated = 0

for root, dirs, files in os.walk('.'):
    if '.git' in root.split(os.sep) or 'node_modules' in root.split(os.sep):
        continue
    for f in files:
        if not f.endswith(exts):
            continue
        path = Path(root) / f
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            new_content = content
            for old, new in replacements:
                new_content = new_content.replace(old, new)
            if new_content != content:
                path.write_text(new_content, encoding='utf-8')
                updated += 1
        except Exception as e:
            print(f"  ERROR: {path} - {e}")

print(f"\nUpdated {updated} code files.")
print("Done! Now run: git add -A && git commit -m 'Rename images to lowercase' && git push")