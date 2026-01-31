import sys
import os

# Add workspace to path
sys.path.append(r"c:\Users\seohy\workspace_antigravity\fortune_guide")

from utils.exchange_banners import get_random_banners, EXCHANGE_BANNERS

def verify_banner_rotation():
    print(f"Total banners available: {len(EXCHANGE_BANNERS)}")
    
    # Run multiple times to check randomization
    for i in range(5):
        selected = get_random_banners(3)
        print(f"\nRun {i+1}:")
        ids = [b['id'] for b in selected]
        print(f"Selected IDs: {ids}")
        
        if len(selected) != 3:
            print("ERROR: Did not return 3 banners")
            return False
            
        if len(set(ids)) != 3:
             print("ERROR: Returned duplicates")
             return False
             
    # Verify 'irumlab' is in the dataset
    irumlab_exists = any(b['id'] == 'irumlab' for b in EXCHANGE_BANNERS)
    if irumlab_exists:
        print("\nSUCCESS: 'irumlab' banner found in configuration.")
    else:
        print("\nERROR: 'irumlab' banner NOT found.")
        return False
        
    return True

if __name__ == "__main__":
    verify_banner_rotation()
