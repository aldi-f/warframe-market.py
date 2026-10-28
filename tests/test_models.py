import msgspec
from warframe_market.models.item import ItemShortModel, ItemModel, ItemI18NModel
from warframe_market.models.order import OrderModel, OrderWithUserModel
from warframe_market.models.activity import ActivityModel, ActivityType
from warframe_market.models.user import UserShortModel, UserModel
from warframe_market.models.lich import (
    LichWeaponModel, LichWeaponI18NModel,
    LichEphemeraModel, LichEphemeraI18NModel,
    LichQuirkModel, LichQuirkI18NModel,
)
from warframe_market.models.sister import (
    SisterWeaponModel, SisterWeaponI18NModel,
    SisterEphemeraModel, SisterEphemeraI18NModel,
    SisterQuirkModel, SisterQuirkI18NModel,
)
from warframe_market.models.riven import RivenModel, RivenAttributeModel
from warframe_market.models.achievement import AchievementModel, AchievementI18NModel, AchievementStateModel
from warframe_market.models.transaction import TransactionModel
from warframe_market.models.dashboard import DashboardShowcaseModel
from warframe_market.models.location import LocationModel
from warframe_market.models.mission import MissionModel
from warframe_market.models.npc import NpcModel
from warframe_market.models.user_private import UserPrivateModel, Role, Tier


# ── Activity ──────────────────────────────────────

class TestActivityModel:
    def test_activity_type_values(self):
        assert ActivityType.ON_MISSION.value == "on_mission"
        assert ActivityType.IN_DOJO.value == "dojo"
        assert ActivityType.UNKNOWN.value == "unknown"
        assert ActivityType.IDLE.value == "idle"
        assert ActivityType.IN_ORBITER.value == "in_orbiter"
        assert ActivityType.IN_RELAY.value == "in_relay"
        assert ActivityType.EMPTY.value == ""

    def test_activity_deserialization(self):
        data = '{"type": "dojo", "details": "The Circuit 55-75", "startedAt": "2024-01-17T22:18:19Z"}'
        act = msgspec.json.decode(data, type=ActivityModel)
        assert act.type == ActivityType.IN_DOJO
        assert act.details == "The Circuit 55-75"

    def test_activity_empty_type(self):
        data = '{"type": "", "details": null, "startedAt": null}'
        act = msgspec.json.decode(data, type=ActivityModel)
        assert act.type == ActivityType.EMPTY

    def test_activity_unknown_type(self):
        data = '{}'
        act = msgspec.json.decode(data, type=ActivityModel)
        assert act.type == ActivityType.UNKNOWN


# ── Item ──────────────────────────────────────────

class TestItemModel:
    def test_item_short_deserialization(self):
        data = '''{
            "id": "54aae292e7798909064f1575",
            "slug": "secura-dual-cestra",
            "gameRef": "/Lotus/Weapons/Syndicates/PerrinSequence/Pistols/PSDualCestra",
            "tags": ["syndicate"],
            "maxRank": 8,
            "maxCharges": 3,
            "vaulted": false,
            "ducats": 45,
            "amberStars": 8,
            "cyanStars": 2,
            "baseEndo": 100,
            "endoMultiplier": 2.0,
            "subtypes": ["blueprint", "crafted"],
            "i18n": {"en": {"name": "Secura Dual Cestra", "icon": "x.png", "thumb": "y.png"}}
        }'''
        item = msgspec.json.decode(data, type=ItemShortModel)
        assert item.id == "54aae292e7798909064f1575"
        assert item.max_rank == 8
        assert item.ducats == 45
        assert item.amber_stars == 8
        assert item.base_endo == 100
        assert item.endo_multiplier == 2.0
        assert "blueprint" in item.subtypes
        assert item.vaulted is False
        assert item.i18n["en"].name == "Secura Dual Cestra"

    def test_item_full_deserialization(self):
        data = '''{
            "id": "x", "slug": "abating_link", "gameRef": "/Lotus/Powersuits/Trinity/LinkAugmentCard",
            "tags": ["mod", "rare"],
            "tradable": true, "vaulted": true,
            "setRoot": false, "setParts": ["a", "b"],
            "quantityInSet": 1,
            "rarity": "rare",
            "maxRank": 9, "maxCharges": 3,
            "baseEndo": 400, "endoMultiplier": 3,
            "bulkTradable": true,
            "maxAmberStars": 5, "maxCyanStars": 10,
            "ducats": 75,
            "reqMasteryRank": 10,
            "tradingTax": 8000,
            "subtypes": ["blueprint"],
            "i18n": {"en": {"name": "Abating Link", "description": "desc", "icon": "x.png", "thumb": "y.png", "wikiLink": "https://wiki"}}
        }'''
        item = msgspec.json.decode(data, type=ItemModel)
        assert item.tradable is True
        assert item.set_root is False
        assert item.rarity == "rare"
        assert item.bulk_tradable is True
        assert item.max_amber_stars == 5
        assert item.req_mastery_rank == 10
        assert item.trading_tax == 8000
        assert item.quantity_in_set == 1
        assert item.i18n["en"].wiki_link == "https://wiki"


# ── Order ─────────────────────────────────────────

class TestOrderModel:
    def test_order_deserialization(self):
        data = '''{
            "id": "ord1", "type": "sell",
            "platinum": 109, "quantity": 1,
            "perTrade": 5, "rank": 10, "charges": 3,
            "subtype": "crafted", "amberStars": 5, "cyanStars": 10,
            "vosfor": 400,
            "visible": true,
            "createdAt": "2016-12-05T17:34:17Z",
            "updatedAt": "2021-05-21T14:59:02Z",
            "itemId": "item1",
            "groupId": "all"
        }'''
        order = msgspec.json.decode(data, type=OrderModel)
        assert order.type == "sell"
        assert order.platinum == 109
        assert order.per_trade == 5
        assert order.rank == 10
        assert order.charges == 3
        assert order.subtype == "crafted"
        assert order.amber_stars == 5
        assert order.cyan_stars == 10
        assert order.vosfor == 400
        assert order.visible is True
        assert order.group_id == "all"
        assert order.item_id == "item1"

    def test_order_minimal_deserialization(self):
        data = '''{
            "id": "ord1", "type": "buy",
            "platinum": 10, "quantity": 5,
            "visible": false,
            "createdAt": "2021-01-01T00:00:00Z",
            "updatedAt": "2021-01-01T00:00:00Z",
            "itemId": "i1"
        }'''
        order = msgspec.json.decode(data, type=OrderModel)
        assert order.type == "buy"
        assert order.vosfor is None
        assert order.per_trade is None
        assert order.rank is None


class TestOrderWithUserModel:
    def test_order_with_user(self):
        data = '''{
            "id": "ord1", "type": "sell",
            "platinum": 100, "quantity": 1,
            "visible": true,
            "createdAt": "2021-01-01T00:00:00Z",
            "updatedAt": "2021-01-01T00:00:00Z",
            "itemId": "i1",
            "user": {
                "id": "uid1", "slug": "player1", "ingameName": "Player1",
                "reputation": 0, "locale": "en",
                "platform": "pc", "crossplay": true,
                "status": "in_game",
                "activity": {"type": "on_mission", "details": "mission1", "startedAt": "2021-01-01T00:00:00Z"},
                "lastSeen": "2021-01-01T00:00:00Z"
            }
        }'''
        order = msgspec.json.decode(data, type=OrderWithUserModel)
        assert order.user.ingame_name == "Player1"
        assert order.user.status == "in_game"
        assert order.user.activity.type == ActivityType.ON_MISSION


# ── Lich ──────────────────────────────────────────

class TestLichModels:
    def test_lich_weapon_i18n_name(self):
        data = '{"name": "Kuva Drakgoon", "icon": "x.png", "thumb": "y.png", "wikiLink": "https://wiki"}'
        obj = msgspec.json.decode(data, type=LichWeaponI18NModel)
        assert obj.name == "Kuva Drakgoon"

    def test_lich_weapon_deserialization(self):
        data = '''{"id":"w1","slug":"kuva_drakgoon","gameRef":"/Lotus/W","reqMasteryRank":13,"i18n":{"en":{"name":"Kuva Drakgoon","icon":"x.png","thumb":"y.png","wikiLink":"https://wiki"}}}'''
        obj = msgspec.json.decode(data, type=LichWeaponModel)
        assert obj.slug == "kuva_drakgoon"
        assert obj.req_mastery_rank == 13
        assert obj.i18n["en"].name == "Kuva Drakgoon"

    def test_lich_weapon_i18n_without_wiki_link(self):
        # The live v2 API omits wikiLink from lich weapon i18n payloads.
        data = '''{"id":"w1","slug":"kuva_drakgoon","gameRef":"/Lotus/W","reqMasteryRank":13,"i18n":{"en":{"name":"Kuva Drakgoon","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=LichWeaponModel)
        assert obj.i18n["en"].wiki_link is None

    def test_lich_ephemera_i18n_name(self):
        data = '{"name": "Vengeful Charge Ephemera", "icon": "x.png", "thumb": "y.png"}'
        obj = msgspec.json.decode(data, type=LichEphemeraI18NModel)
        assert obj.name == "Vengeful Charge Ephemera"

    def test_lich_ephemera(self):
        data = '''{"id":"e1","slug":"vengeful_charge","gameRef":"/Lotus/Upgrades/...","animation":"a.webp","element":"electricity","i18n":{"en":{"name":"Vengeful Charge Ephemera","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=LichEphemeraModel)
        assert obj.animation == "a.webp"
        assert obj.element == "electricity"

    def test_lich_quirk_i18n_name(self):
        data = '{"name": "Poor Sense of Balance", "description": "The lich will retreat", "icon": "x.png", "thumb": "y.png"}'
        obj = msgspec.json.decode(data, type=LichQuirkI18NModel)
        assert obj.name == "Poor Sense of Balance"
        assert obj.description == "The lich will retreat"

    def test_lich_quirk(self):
        data = '''{"id":"q1","slug":"poor_sense_of_balance","group":"default","i18n":{"en":{"name":"Poor Sense of Balance","description":"The lich will retreat","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=LichQuirkModel)
        assert obj.group == "default"


# ── Sister ────────────────────────────────────────

class TestSisterModels:
    def test_sister_weapon_i18n_name(self):
        data = '{"name": "Tenet Tetra", "icon": "x.png", "thumb": "y.png", "wikiLink": "https://wiki"}'
        obj = msgspec.json.decode(data, type=SisterWeaponI18NModel)
        assert obj.name == "Tenet Tetra"

    def test_sister_weapon(self):
        data = '''{"id":"w1","slug":"tenet_tetra","gameRef":"/Lotus/Weapons/...","reqMasteryRank":16,"i18n":{"en":{"name":"Tenet Tetra","icon":"x.png","thumb":"y.png","wikiLink":"https://wiki"}}}'''
        obj = msgspec.json.decode(data, type=SisterWeaponModel)
        assert obj.req_mastery_rank == 16

    def test_sister_ephemera_i18n_name(self):
        data = '{"name": "Gloriana Ephemera", "icon": "x.png", "thumb": "y.png"}'
        obj = msgspec.json.decode(data, type=SisterEphemeraI18NModel)
        assert obj.name == "Gloriana Ephemera"

    def test_sister_quirk_i18n_name(self):
        data = '{"name": "Coward", "description": "Can leave the mission at low health", "icon": "x.png", "thumb": "y.png"}'
        obj = msgspec.json.decode(data, type=SisterQuirkI18NModel)
        assert obj.name == "Coward"


# ── Riven ─────────────────────────────────────────

class TestRivenModels:
    def test_riven_deserialization(self):
        data = '''{"id":"r1","slug":"kulstar","gameRef":"/Lotus/W","group":"secondary","rivenType":"pistol","disposition":1.3,"reqMasteryRank":5,"i18n":{"en":{"name":"Kulstar","icon":"x.png","thumb":"y.png","wikiLink":"https://wiki","subIcon":"s.png"}}}'''
        obj = msgspec.json.decode(data, type=RivenModel)
        assert obj.disposition == 1.3
        assert obj.riven_type == "pistol"
        assert obj.group == "secondary"

    def test_riven_i18n_without_sub_icon(self):
        # The live v2 API omits subIcon/wikiLink from riven i18n payloads.
        data = '''{"id":"r1","slug":"kulstar","gameRef":"/Lotus/W","group":"secondary","rivenType":"pistol","disposition":1.3,"reqMasteryRank":5,"i18n":{"en":{"name":"Kulstar","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=RivenModel)
        assert obj.i18n["en"].sub_icon is None
        assert obj.i18n["en"].wiki_link is None

    def test_riven_attribute(self):
        data = '''{"id":"a1","slug":"recoil","gameRef":"WeaponRecoil","group":"default","prefix":"Zeti","suffix":"Mag","exclusiveTo":["shotgun","rifle"],"positiveIsNegative":true,"positiveOnly":true,"unit":"percent","i18n":{"en":{"name":"Weapon Recoil","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=RivenAttributeModel)
        assert obj.prefix == "Zeti"
        assert obj.suffix == "Mag"
        assert obj.positive_is_negative is True
        assert obj.positive_only is True
        assert obj.unit == "percent"


# ── Achievement ───────────────────────────────────

class TestAchievementModel:
    def test_achievement_with_state(self):
        data = '''{"id":"a1","slug":"github_contribution","type":"github","goal":5,"state":{"featured":true,"progress":3,"completedAt":"2025-01-01T00:00:00Z"}}'''
        obj = msgspec.json.decode(data, type=AchievementModel)
        assert obj.slug == "github_contribution"
        assert obj.goal == 5
        assert obj.state is not None
        assert obj.state.featured is True
        assert obj.state.progress == 3
        assert obj.state.completed_at == "2025-01-01T00:00:00Z"

    def test_achievement_without_state(self):
        data = '''{"id":"a1","slug":"test","type":"test","goal":5}'''
        obj = msgspec.json.decode(data, type=AchievementModel)
        assert obj.state is None


# ── Transaction ───────────────────────────────────

class TestTransactionModel:
    def test_transaction_with_user(self):
        data = '''{"id":"txn1","type":"sell","originId":"ord1","platinum":33,"quantity":6,"createdAt":"2025-01-01T00:00:00Z","updatedAt":"2025-01-01T00:00:00Z","item":{"id":"item1","rank":5,"charges":3,"subtype":"crafted","cyanStars":2,"amberStars":1},"user":{"id":"uid1","slug":"p1","ingameName":"Player1","reputation":0,"locale":"en","platform":"pc","crossplay":true,"status":"online","activity":{"type":"idle","details":null,"startedAt":null},"lastSeen":"2025-01-01T00:00:00Z"}}'''
        obj = msgspec.json.decode(data, type=TransactionModel)
        assert obj.origin_id == "ord1"
        assert obj.item.rank == 5
        assert obj.item.charges == 3
        assert obj.item.subtype == "crafted"
        assert obj.user is not None
        assert obj.user.ingame_name == "Player1"

    def test_transaction_without_user(self):
        data = '''{"id":"txn1","type":"sell","originId":"ord1","platinum":33,"quantity":6,"createdAt":"2025-01-01T00:00:00Z","updatedAt":"2025-01-01T00:00:00Z","item":{"id":"item1","rank":5}}'''
        obj = msgspec.json.decode(data, type=TransactionModel)
        assert obj.user is None


# ── Dashboard ─────────────────────────────────────

class TestDashboardShowcaseModel:
    def test_dashboard(self):
        data = '''{"i18n":{"en":{"title":"Xaku Prime Access","description":"Xaku Prime Access is here!"}},"items":[{"item":"id1","background":"showcase/xakuPrime.webp","bigCard":true},{"item":"id2","background":"showcase/x.webp","bigCard":false}]}'''
        obj = msgspec.json.decode(data, type=DashboardShowcaseModel)
        assert obj.i18n["en"].title == "Xaku Prime Access"
        assert obj.items[0].big_card is True
        assert obj.items[1].big_card is False
        assert obj.items[0].background == "showcase/xakuPrime.webp"


# ── Location / Mission / NPC ──────────────────────

class TestLocationModel:
    def test_location(self):
        data = '''{"id":"l1","slug":"amarna","gameRef":"ClanNode14","faction":"infested","minLevel":35,"maxLevel":45,"i18n":{"en":{"nodeName":"Amarna","systemName":"Sedna","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=LocationModel)
        assert obj.faction == "infested"
        assert obj.min_level == 35
        assert obj.max_level == 45
        assert obj.i18n["en"].node_name == "Amarna"
        assert obj.i18n["en"].system_name == "Sedna"


class TestMissionModel:
    def test_mission(self):
        data = '''{"id":"m1","slug":"level_50_70_orb_vallis_bounty","gameRef":"","i18n":{"en":{"name":"Level 50 - 70 Orb Vallis Bounty","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=MissionModel)
        assert obj.i18n["en"].name == "Level 50 - 70 Orb Vallis Bounty"


class TestNpcModel:
    def test_npc(self):
        data = '''{"id":"n1","slug":"infested_grineer","gameRef":"","i18n":{"en":{"name":"Infested Grineer","icon":"x.png","thumb":"y.png"}}}'''
        obj = msgspec.json.decode(data, type=NpcModel)
        assert obj.i18n["en"].name == "Infested Grineer"


# ── User / UserPrivate ────────────────────────────

class TestUserShortModel:
    def test_user_short(self):
        data = '''{"id":"uid1","ingameName":"Player1","slug":"player1","avatar":"avatar.png","reputation":0,"locale":"en","platform":"pc","crossplay":true,"status":"in_game","activity":{"type":"dojo","details":"The Circuit 55-75","startedAt":"2024-01-17T22:18:19Z"},"lastSeen":"2024-01-17T22:18:19Z"}'''
        obj = msgspec.json.decode(data, type=UserShortModel)
        assert obj.ingame_name == "Player1"
        assert obj.slug == "player1"
        assert obj.crossplay is True
        assert obj.activity.type == ActivityType.IN_DOJO


class TestUserModel:
    def test_user_full(self):
        data = '''{"id":"uid1","ingameName":"Player1","slug":"player1","avatar":"avatar.png","background":"bg.png","about":"<p>bio</p>","reputation":10,"masteryLevel":20,"platform":"pc","crossplay":true,"locale":"en","status":"in_game","activity":{"type":"idle","details":null,"startedAt":null},"lastSeen":"2024-01-17T22:18:19Z","banned":true,"banUntil":"2074-01-17T00:00:00Z","warned":true,"warnMessage":"warning","banMessage":"banned","achievementShowcase":[{"id":"ach1","icon":"icon.png","thumb":"thumb.png","type":"patreon","i18n":{"en":{"name":"Platinum Patron","description":"desc"}}}]}'''
        obj = msgspec.json.decode(data, type=UserModel)
        assert obj.ingame_name == "Player1"
        assert obj.mastery_level == 20
        assert obj.banned is True
        assert obj.ban_until == "2074-01-17T00:00:00Z"
        assert obj.banned is True
        assert len(obj.achievement_showcase) == 1
        assert obj.achievement_showcase[0].type == "patreon"


class TestUserPrivateModel:
    def test_user_private_role_tier(self):
        assert Role.USER == "user"
        assert Role.MODERATOR == "moderator"
        assert Role.ADMIN == "admin"
        assert Tier.NONE == "none"
        assert Tier.BRONZE == "bronze"
        assert Tier.SILVER == "silver"
        assert Tier.GOLD == "gold"
        assert Tier.PLATINUM == "platinum"
        assert Tier.DIAMOND == "diamond"