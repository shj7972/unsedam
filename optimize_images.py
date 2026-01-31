import os
from PIL import Image
import glob

def optimize_images():
    """타로 이미지를 WebP로 변환하고 크기를 조정하여 용량을 대폭 줄입니다."""
    target_dir = 'static/images/tarot'
    images = glob.glob(os.path.join(target_dir, '*.png'))
    
    print(f"총 {len(images)}개의 타로 이미지 최적화 시작...")
    
    total_saved = 0
    max_width = 600
    
    for img_path in images:
        try:
            with Image.open(img_path) as img:
                # 파일 사이즈 체크 (전)
                size_before = os.path.getsize(img_path)
                
                # 크기 조정 (너비 기준 max_width로 맞춤)
                if img.width > max_width:
                    ratio = max_width / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # RGBA를 RGB로 변환 (WebP는 투명도를 지원하지만 여기서는 필요 없음)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # WebP로 저장
                webp_path = os.path.splitext(img_path)[0] + '.webp'
                img.save(webp_path, "WEBP", quality=80)
                
                # 파일 사이즈 체크 (후)
                size_after = os.path.getsize(webp_path)
                saved = (size_before - size_after) / (1024 * 1024)
                total_saved += saved
                
                print(f"최적화 완료: {os.path.basename(img_path)} -> {os.path.basename(webp_path)} ({size_before/1024/1024:.1f}MB -> {size_after/1024/1024:.1f}MB)")
                
                # 원본 PNG 파일 삭제 (선택 사항, 여기서는 성능을 위해 삭제)
                # os.remove(img_path)
                
        except Exception as e:
            print(f"에러 발생 ({img_path}): {e}")

    # 메인 OG 이미지 최적화
    og_image = 'static/images/og-image.png'
    if os.path.exists(og_image):
        try:
            with Image.open(og_image) as img:
                # OG 이미지도 WebP로 변환 고려 가능하나, 소셜 공유 호환성을 위해 PNG 유지하며 압축
                if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                size_before = os.path.getsize(og_image)
                
                # 너무 크면 리사이즈 (OG 이미지는 보통 1200x630 권장)
                if img.width > 1200:
                    ratio = 1200 / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
                
                img.save(og_image, "PNG", optimize=True)
                size_after = os.path.getsize(og_image)
                print(f"최적화 완료: og-image.png ({size_before/1024/1024:.1f}MB -> {size_after/1024/1024:.1f}MB)")
        except Exception as e:
            print(f"에러 발생 (og-image): {e}")

    print(f"\n총 약 {total_saved:.1f}MB 용량을 절약했습니다.")

if __name__ == "__main__":
    optimize_images()
