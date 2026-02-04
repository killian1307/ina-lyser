# TRANSLATION DICTIONARY
class LangDict:
    def __init__(self, lang_code="en"):
        self.lang = lang_code
        self.dict_all_languages = {
            "en": {
                "header": "Export your Victory Road teams to JSON.",
                "tabs": ["Scanner", "Read Me"],
                "db_error": "❌ Database not found. Please check your folder structure.",
                "upload_label": "Upload a screenshot",
                "uploaded_caption": "Uploaded Image",
                "scan_button": "⚡ Scan Team",
                "spinner": "Scanning team...",
                "no_players": "No players found. Try a clearer screenshot.",
                "instructions_title": "### How to use Ina-lyser",
                "step_1": "1. **Launch Inazuma Eleven: Victory Road** and go to the **Formation** screen.",
                "step_2": "2. **Press the Nickname button** (x on keyboard) to ensure full names are shown (works with Japanese AND international names).",
                "step_3": "3. **Take a clear screenshot** (Exactly like shown in the example below).",
                "step_4": "4. **Upload the image** in the 'Scanner' tab.",
                "step_5": "5. **Download the JSON** file to share your team!",
                "tip": "💡 **Tip:** For best results, try switching text names to english (not mandatory but recommended for layouts detection).",
                "warning": "⚠️ **Warning:** Using your Original Character isn't supported by the algorithm, but it will still go through, leaving your coach as blank. Just keep that in mind when importing.",
                "example_caption": "Example of a good screenshot",
                "example_missing": "Add an example screenshot to see it here.",
                "download_label": "Download JSON"
            },
            "fr": {
                "header": "Exportez vos équipes Victory Road au format JSON.",
                "tabs": ["Scanner", "Mode d'emploi"],
                "db_error": "❌ Base de données introuvable. Vérifiez l'architecture du dossier.",
                "upload_label": "Télécharger une capture d'écran",
                "uploaded_caption": "Image téléchargée",
                "scan_button": "⚡ Scanner l'équipe",
                "spinner": "Analyse de l'équipe...",
                "no_players": "Aucun joueur trouvé. Essayez une capture plus claire.",
                "instructions_title": "### Comment utiliser Ina-lyser",
                "step_1": "1. **Lancez Inazuma Eleven: Victory Road** et allez dans le menu **Formation**.",
                "step_2": "2. **Appuyez sur le bouton Surnom** (x sur le clavier) pour afficher les noms complets (fonctionne avec les noms japonais ET internationaux).",
                "step_3": "3. **Prenez une capture d'écran claire** (Exactement comme l'exemple ci-dessous).",
                "step_4": "4. **Importez l'image** dans l'onglet 'Scanner'.",
                "step_5": "5. **Téléchargez le fichier JSON** pour partager votre équipe !",
                "tip": "💡 **Conseil :** Pour de meilleurs resultats, essayez de mettre les textes du jeu en anglais (pas obligatoire mais à essayer si la reconnaissance de formation ne fonctionne pas).",
                "warning": "⚠️ **Attention :** Si vous jouez votre propre personnage, cela n'apparaitra pas dans le fichier exporté. Votre emplacement de coach sera considéré comme vide par défaut. Gardez ça à l'esprit lors de l'import de vos données.",
                "example_caption": "Exemple d'une bonne capture d'écran",
                "example_missing": "Ajoutez une capture d'exemple pour la voir ici.",
                "download_label": "Télécharger JSON"
            }
        }
        
        self.current_dict = self.dict_all_languages.get(self.lang, self.dict_all_languages["en"])
    
    def get_next_lang_code(self):
        return "fr" if self.lang == "en" else "en"
