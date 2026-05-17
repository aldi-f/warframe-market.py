from warframe_market.common.enums import Language, Platform, Subtype


class TestLanguage:
    def test_values(self):
        assert Language.KOREAN.value == "ko"
        assert Language.RUSSIAN.value == "ru"
        assert Language.GERMAN.value == "de"
        assert Language.FRENCH.value == "fr"
        assert Language.PORTUGUESE.value == "pt"
        assert Language.CHINESE_SIMPLIFIED.value == "zh-hans"
        assert Language.CHINESE_TRADITIONAL.value == "zh-hant"
        assert Language.SPANISH.value == "es"
        assert Language.ITALIAN.value == "it"
        assert Language.POLISH.value == "pl"
        assert Language.UKRAINIAN.value == "uk"
        assert Language.ENGLISH.value == "en"


class TestPlatform:
    def test_values(self):
        assert Platform.PC.value == "pc"
        assert Platform.PS4.value == "ps4"
        assert Platform.XBOX.value == "xbox"
        assert Platform.SWITCH.value == "switch"
        assert Platform.MOBILE.value == "mobile"


class TestSubtype:
    def test_values(self):
        assert Subtype.BLUEPRINT.value == "blueprint"
        assert Subtype.CRAFTED.value == "crafted"