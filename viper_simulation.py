import re


class VIPERTopologyEvaluator:
    def __init__(self):
        self.state = "THINK"
        self.scar_archive = {
            "β1": "+++SpatialBind(RCC8='Disconnected', Parallax_Z='≥10cm')",
            "β2": "+++HardwareForcedPhysicality(Key_Direction='specified_azimuth_elevation')",  # noqa: E501
            "β3": "+++SpatialBind(RCC8='Externally_Connected', Contact_Normal='floor_plane')",  # noqa: E501
            "β4": "+++MereologyRoute(relation_type='Part-Whole', transitivity_check=true)",  # noqa: E501
            "β5": "+++AdjectivalBound(max_per_entity=1) + +++HardwareForcedPhysicality(Film_Stock='high_grain_stock')"  # noqa: E501
        }
        self.banned_tokens = {
            "masterpiece", "epic", "stunning", "beautiful", "hyper-realistic",
            "trending on artstation", "8k", "4k", "ultra HD", "cinematic vibes",  # noqa: E501
            "moody", "ethereal", "perfect", "flawless", "amazing", "breathtaking",  # noqa: E501
            "gorgeous", "cinematic"
        }
        self.active_scars = set()

    def advance_state(self, new_state: str):
        # Strict state machine progression
        valid_transitions = {
            "THINK": "DENOISE",
            "DENOISE": "PHYSICALIZE",
            "PHYSICALIZE": "EXTRUDE"
        }
        if self.state in valid_transitions and valid_transitions[self.state] == new_state:  # noqa: E501
            self.state = new_state
        else:
            raise ValueError(
                f"Invalid Petzold Sequence transition from {self.state} to {new_state}")  # noqa: E501

    def calculate_ads(self, text: str) -> float:
        """
        Calculates Adjectival Dilution Score (ADS).
        A mock implementation since true POS tagging requires NLP libraries.
        We'll simulate it by counting adjectives and nouns roughly.
        """
        # For simulation, we'll assume words ending in certain suffixes or in a list are adjectives  # noqa: E501
        mock_adjectives = ["old", "dark", "heavy",
                           "nicotine-stained", "single", "condensation-streaked"]  # noqa: E501
        mock_nouns = ["woman", "portrait", "cafe", "coat", "brasserie", "interior", "walls", "floor", "window", "particulate",  # noqa: E501
                      "haze", "backlight", "halation", "edges", "practicals", "subject", "table", "wardrobe", "environment", "atmosphere"]  # noqa: E501

        words = re.findall(r'\b\w+(?:-\w+)?\b', text.lower())
        adj_count = sum(1 for w in words if w in mock_adjectives)
        noun_count = sum(1 for w in words if w in mock_nouns)

        if noun_count == 0:
            return 0.0
        return adj_count / noun_count

    def apply_banned_token_protocol(self, text: str) -> list:
        """
        Checks for banned tokens and returns a list of rejected tokens.
        """
        rejected = []
        lower_text = text.lower()
        for token in self.banned_tokens:
            if token in lower_text:
                rejected.append(token)
        return rejected

    def validate_hgi(self, hfp_decorator: str) -> bool:
        """
        Validates Hardware Grounding Index (HGI).
        Must contain Lens, and (Aperture OR Film_Stock), and Lighting.
        """
        has_lens = "Lens=" in hfp_decorator
        has_aperture_or_stock = "Aperture=" in hfp_decorator or "Film_Stock=" in hfp_decorator  # noqa: E501
        has_lighting = "Lighting=" in hfp_decorator

        return has_lens and has_aperture_or_stock and has_lighting

    def enforce_spatial_bind(self, subjects: list) -> list:
        """
        Returns SpatialBind decorators if there are multiple subjects.
        """
        bindings = []
        if len(subjects) >= 2:
            # Example mock binding
            bindings.append(
                f"+++SpatialBind(Subject_A='{subjects[0]}', Subject_B='{subjects[1]}', RCC8='Disconnected')")  # noqa: E501
        return bindings

    def process_prompt(self, user_prompt: str) -> dict:
        """
        Simulates the Immune-Aware Petzold Loop.
        """
        self.state = "THINK"

        # PHASE 1: THINK
        # Simulate CFDI check and Scars
        cfdi = 0.10  # Mock value
        if cfdi > 0.15:
            raise Exception("EpistemicEscrow Triggered: CFDI > 0.15")

        self.advance_state("DENOISE")

        # PHASE 2: DENOISE
        rejected_tokens = self.apply_banned_token_protocol(user_prompt)
        # Strip banned tokens for calculation
        stripped_prompt = user_prompt
        for token in rejected_tokens:
            stripped_prompt = stripped_prompt.replace(token, "")

        ads_post_strip = self.calculate_ads(stripped_prompt)
        if ads_post_strip > 0.15:
            return {"status": "HALT", "reason": f"ADS post-strip > 0.15 ({ads_post_strip})"}  # noqa: E501

        self.advance_state("PHYSICALIZE")

        # PHASE 3: PHYSICALIZE
        # Mock mapping to HFP
        hfp = "+++HardwareForcedPhysicality(Lens='Cooke S4/i 40mm', Aperture='T2.8', Film_Stock='CineStill 800T', Lighting='Practical tungsten sconce lamps, 2700K', Sensor='Super35')"  # noqa: E501
        hgi_valid = self.validate_hgi(hfp)

        if not hgi_valid:
            return {"status": "HALT", "reason": "HGI Non-Compliant"}

        self.advance_state("EXTRUDE")

        # PHASE 4: EXTRUDE
        return {
            "status": "SUCCESS",
            "OSM": {
                "Base_Syntax": stripped_prompt.strip(),
                "ADS_Final": ads_post_strip,
                "HGI_Final": "100%",
                "Rejected_Tokens": rejected_tokens
            }
        }
