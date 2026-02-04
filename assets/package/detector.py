import easyocr
import pandas as pd
import json
import os
import cv2
import re
import time

class ExactTeamScanner:
    def __init__(self, csv_path, image_path):
        self.csv_path = csv_path
        self.image_path = image_path
        self.reader = easyocr.Reader(['en'], gpu=False) 
        
        self.db = self.load_database()
        
        self.callback = None  # Holder for the website function

    # If called, then it's running from the website
    def set_callback(self, func):
        self.callback = func
            
    # Custom log function
    def log(self, message):
        if self.callback:
            self.callback(message) # Send to website UI
            time.sleep(0.02)
        else:
            print(message) # Send to console
        
    def load_database(self):
        """
        Loads the CSV and creates a lookup for Full Names and Flipped Names.
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
            
        df = pd.read_csv(self.csv_path)
        lookup = {}
        
        for _, row in df.iterrows():
            romaji = str(row['Name(Romaji)']).strip()
            local = str(row['Name(Localised)']).strip()
            
            player_data = {
                'id': int(row['ID']),
                'name': romaji,            
                'name_localised': local,
                'position': row['Position'],
                'element': row['Element'],
                'stats': row['Total Stats']
            }
            
            # Add Exact Names to the dictionnary
            lookup[romaji.lower()] = player_data
            lookup[local.lower()] = player_data

        return lookup

    def preprocess_image(self):
        """ Upscale x2 and increase contrast """
        img = cv2.imread(self.image_path)
        if img is None:
            raise ValueError(f"Could not load image: {self.image_path}")
        
        img_large = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        # Increase contrast
        contrast_img = cv2.convertScaleAbs(img_large, alpha=1.5, beta=-70)
        # DEBUG: saves the contrasted image
        # cv2.imwrite("debug_high_contrast.jpg", contrast_img)
        return contrast_img

    def get_reading_order(self, result):
        """
        Sorts boxes by Y-coordinate first (with tolerance), then X-coordinate.
        This ensures 'Yuya' (left) comes before 'Kogure' (right) on the same line.
        """
        bbox = result[0]
        y_top = bbox[0][1]
        x_left = bbox[0][0]
        
        # Group Y-coordinates into 20px "lines" to handle slight misalignments
        y_line = int(y_top / 20) * 20 
        return (y_line, x_left)

    def scan(self):
        self.log(f"Scanning image...")
        processed_img = self.preprocess_image()
        
        # width_ths=0.7 helps merge words that are close, but we do manual stitching too
        results = self.reader.readtext(processed_img, detail=1, width_ths=0.7)
        
        # Sort by Reading Order
        results.sort(key=self.get_reading_order)
        
        found_players = []
        formation_text = None
        formation_id = None
        found_formation = (None, None)
        
        seen_ids = set()
        
        # Extract text list
        text_list = [r[1].strip() for r in results]
        
        # DEBUG: RAW LIST
        # print("\n--- [DEBUG] Full Detected Text List (Sorted) ---")
        # for idx, t in enumerate(text_list):
        #     self.log(f"[{idx}] {t}")
        self.log("------------------------------------------------\n")
        
        i = 0
        while i < len(text_list):
            
            # Checks for unwanted chars
            characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 123456" # ADD "-" IF FORMATION GLITCHES OUT
            
            formations = ["442", "352", "433", "451", "361", "541"]
            # WITH DASHES IF FORMATION GLITCHES OUT
            # formations = ["4-4-2", "3-5-2", "4-3-3", "4-5-1", "3-6-1", "5-4-1"]
            
            match_found = False
            player_found = None
            
            current_text = ""
            for char in text_list[i]:
                if char in characters:
                    current_text+=char
            current_text = current_text.strip()
            
            # Checks for formation before lowering
            for j in range(len(formations)):
                if formations[j] in current_text:
                    formation_text=current_text
                    formation_id=j
                    match_found = True
                    i+=1
            
            current_text=current_text.lower()
            
            # LOGIC TRACE
            self.log(f"👉 Index {i}: Processing '{current_text}'")

            # OPTION 1: Try combining with NEXT word
            if i + 1 < len(text_list):
                next_text = text_list[i+1].lower()
                combined_text = f"{current_text} {next_text}"
                
                if combined_text in self.db:
                    player_found = self.db[combined_text]
                    self.log(f"      ✅ STITCHED MATCH! -> Found ID: {player_found['id']} ({player_found['name']})")
                    i += 2 # Skip next word
                    match_found = True
            
            # OPTION 2: If Stitch failed, try SINGLE word
            if not match_found:
                
                if current_text in self.db:
                    player_found = self.db[current_text]
                    self.log(f"      ✅ SINGLE MATCH! -> Found ID: {player_found['id']} ({player_found['name']})")
                    i += 1
                    match_found = True
            
            # If still no match
            if not match_found:
                i += 1
                
            # Add to found list
            if match_found and player_found:
                if player_found['id'] not in seen_ids:
                    found_players.append(player_found)
                    seen_ids.add(player_found['id'])
            # If only match found, then we found a formation
            elif match_found:
                self.log(f"      ✅ FORMATION FOUND! -> {formation_text}")
                found_formation=(formation_text, formation_id)
            
            self.log("   ----------------")
        
        final_formation=self.detect_formation(found_formation[0], found_formation[1])
        return found_players, final_formation
    
    def detect_formation(self, text, id):
        
        # ID list
        # 0 : 4-4-2 Diamond }          0
        # 1 : 4-4-2 Box     }
        # 2 : 3-5-2 Freedom            1
        # 3 : 4-3-3 Triangle }         2
        # 4 : 4-3-3 Delta    }
        # 5 : 4-5-1 Balanced           3
        # 6 : 3-6-1 Hexa               4
        # 7 : 5-4-1 Double Volante     5
        formations_list=["4-4-2 Diamond", "4-4-2 Box", "3-5-2 Freedom", "4-3-3 Triangle", "4-3-3 Delta", "4-5-1 Balanced", "3-6-1 Hexa", "5-4-1 Double Volante"]

        if text == None and id == None:
            return formations_list[0], 0
        # If the ID doesn't represent 2 possible formations
        if id in [3, 4, 5]:
            return (formations_list[id+2], id+2)
        elif id == 1:
            return (formations_list[id+1], id+1)
        # Most complex case: the id could be 2 formations because their player numbers match
        else:
            text=text.lower()
            if "442" in text:
                # Check Text Keywords (Multi-lang substrings)
                if "dia" in text:
                    return formations_list[0], 0
                if "bo" in text:
                    return formations_list[1], 1
            if "433" in text:
                # Check Text Keywords (Multi-lang substrings)
                if "trian" in text:
                    return formations_list[3], 3
                if "delt" in text:
                    return formations_list[4], 4
        # If nothing else worked, return the first formation
        return formations_list[0], 0

    def export_json(self, players, formation):
        count = len(players)
        self.log(f"\n--- LOGIC CHECK: Found {count} players ---")
        
        coach_name = "None"
        final_team = players
        
        count = len(players)
        # If we have 12 players, there is a coach that isn't the OC character
        if count >= 12:
                # Almost all formations make the program read some FW before the coach
                if formation[1] in [1]:
                    coach_name = players[2]['name']
                    final_team=final_team[:2]+final_team[3:]
                    
                elif formation[1] in [2, 3, 4, 5, 6]:
                    coach_name = players[1]['name']
                    final_team=[final_team[0]]+final_team[2:]

                else:
                    coach_name = players[0]['name']
                    final_team=final_team[1:]
                
                self.log(f"👉 Auto-Logic: Coach is {coach_name}")

        data = {
            "team_count": len(final_team),
            "coach": coach_name,
            "formation_structure": [p['name'] for p in final_team],
            "formation_layout": formation[0]
        }
        
        # Deprecated export
#         with open('../../exports/team_export.json', 'w', encoding='utf-8') as f:
#             json.dump(data, f, indent=4, ensure_ascii=False)
        self.log("🎉 Done! Download your team_export.json below.")
        return data

if __name__ == "__main__":
    CSV_FILE = "../players/db.csv"
    IMG_FILE = "../../test_screenshots/3.png"
    try:
        scanner = ExactTeamScanner(CSV_FILE, IMG_FILE)
        team = scanner.scan()
        # DEBUG: print team
        # print(team)
        if team:
            scanner.export_json(team[0], team[1])
        else:
            print("❌ No players found.")
    except Exception as e:

        print(f"Error: {e} - COULDN'T OUTPUT FILE.")
