# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, ForeignKey, Integer, Numeric, String, \
    Text, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()
metadata = Base.metadata


class ClientProgramHotels6(Base):
    __tablename__ = 'ClientProgramHotels6'

    Id = Column(BigInteger, primary_key=True)
    ClientProgramsId = Column(BigInteger)
    Hotel_PropertyId = Column(BigInteger)
    HotelStatus = Column(String(255))
    ConsultantRecommendation = Column(String(255))
    ClientResponse = Column(String(255))
    DynamicPricingRecommended = Column(String(255))
    ActivityCount = Column(String(255))
    SpendTotalUsd = Column(String(255))
    RoomNightsTotal = Column(String(255))
    IsPreferred = Column(String(255))
    ABR = Column(String(255))
    ANR = Column(String(255))
    BCD = Column(String(255))
    MarketShare = Column(String(255))
    PyBid = Column(String(255))
    RateAvailability = Column(String(255))
    LosGreaterThan5 = Column(String(255))
    CountConsultantComments = Column(String(255))
    LastConsultantComment = Column(String(255))
    CountClientComments = Column(String(255))
    LastClientComment = Column(String(255))
    PyIsDynamicPricing = Column(String(255))
    CountFreeComments = Column(String(255))
    CountBatchComments = Column(String(255))
    CountSmartSelectComments = Column(String(255))
    L = Column(String(255))
    HotelStatusDatetime = Column(String(255))
    RoomNightsPy = Column(String(255))
    Created = Column(String(255))
    Modified = Column(String(255))
    BidStatus = Column(String(255))
    BidConsultantRecommendation = Column(String(255))
    BidClientRecommendation = Column(String(255))
    BidInfo = Column(String(255))
    PaShareStatus = Column(String(255))
    AmenitiesBreakfast = Column(String(255))
    AmenitiesHsia = Column(String(255))
    AmenitiesWifi = Column(String(255))
    AmenitiesParking = Column(String(255))
    AmenitiesAirportTx = Column(String(255))
    AmenitiesOfficeTx = Column(String(255))
    AmenitiesFitness = Column(String(255))
    AmenitiesLocalPhone = Column(String(255))
    AmenitiesTollPhone = Column(String(255))
    FeeVatIncluded = Column(String(255))
    FeeServiceIncluded = Column(String(255))
    FeeLodgeTaxIncluded = Column(String(255))
    FeeStateTaxIncluded = Column(String(255))
    FeeCityTaxIncluded = Column(String(255))
    FeeOccIncluded = Column(String(255))
    FeeOtherIncluded = Column(String(255))
    CountPaConsultantComments = Column(String(255))
    CountPaClientComments = Column(String(255))
    CountPaActivity = Column(String(255))
    BidReadOnly = Column(String(255))
    DistanceClosestMiles = Column(String(255))
    CountPaClientActivity = Column(String(255))
    Anr_Lanyon = Column(String(255))
    Anr_LanyonCurrencyCode = Column(String(255))
    Anr_Dynamic = Column(String(255))
    IsReviewedClient = Column(String(255))
    isReviewedConsultant = Column(String(255))
    modifiedLabel = Column(String(255))


class DebugLog(Base):
    __tablename__ = 'debuglog'

    id = Column(BigInteger, primary_key=True)
    logtime = Column(TIMESTAMP(precision=6))
    eventtype = Column(BigInteger)
    event = Column(Text)


class FilterSet(Base):
    __tablename__ = 'filter_set'

    id = Column(BigInteger, primary_key=True)
    filter_clause = Column(Text)
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    modified = Column(DateTime, nullable=False, server_default=text("now()"))


class HotelChain(Base):
    __tablename__ = 'hotel_chain'

    id = Column(BigInteger, primary_key=True)
    chain_name = Column(String(64), nullable=False)
    chain_tag = Column(String(16))
    chain_note = Column(Text)
    holding_company_name = Column(String(64))
    chain_code_sabre = Column(String(8))
    chain_code_amadeus = Column(String(8))
    chain_code_galileo = Column(String(8))
    chain_code_worldspan = Column(String(8))
    chain_code_master = Column(String(8))
    market_tier_code = Column(String(8))
    market_tier_label = Column(String(32))
    service_level = Column(String(16))
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    modified = Column(DateTime, nullable=False, server_default=text("now()"))


class HotelProperty(Base):
    __tablename__ = 'hotel_property'

    id = Column(BigInteger, primary_key=True)
    hotel_chain_id = Column(ForeignKey('hotel_chain.id'))
    property_name = Column(String(128))
    property_tag = Column(String(32))
    property_note = Column(Text)
    id_hmf = Column(BigInteger)
    id_lanyon = Column(String(32))
    id_max = Column(String(32))
    id_travelclick = Column(String(32))
    id_amadeus = Column(String(32))
    id_apollo = Column(String(32))
    id_sabre = Column(String(32))
    id_worldspan = Column(String(32))
    address1 = Column(String(128))
    address2 = Column(String(128))
    city = Column(String(64))
    state = Column(String(8))
    postal_code = Column(String(32))
    geo_city_id = Column(BigInteger, index=True)
    geo_state_id = Column(BigInteger, index=True)
    geo_country_id = Column(BigInteger, index=True)
    regions_id = Column(BigInteger)
    latitude = Column(Float(53))
    longitude = Column(Float(53))
    phone_primary = Column(String(64))
    phone_fax = Column(String(64))
    website = Column(String(128))
    email_primary = Column(String(128))
    minority_owner_code = Column(Integer)
    country = Column(String(64))
    olset_rating = Column(Float(53))
    id_advito_property_2005 = Column(BigInteger)
    created = Column(TIMESTAMP(precision=0), server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=0), server_default=text("now()"))

    hotel_chain = relationship('HotelChain')


class LanyonFeed(Base):
    __tablename__ = 'lanyon_feed'

    id = Column(BigInteger, primary_key=True)
    feed_filename = Column(String(128))
    feed_datetime = Column(TIMESTAMP(precision=6))
    import_status = Column(String(32))
    import_note = Column(Text)
    count_bids_added = Column(Integer)
    count_bids_error = Column(Integer)
    count_bids_skipped = Column(Integer)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class Program(Base):
    __tablename__ = 'program'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(BigInteger, nullable=False)
    program_name = Column(String(64), nullable=False)
    program_year = Column(Integer)
    program_status = Column(String(32))
    program_phase = Column(String(32))
    program_note = Column(Text)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    pa_is_enabled = Column(Boolean, server_default=text("false"))
    date_program_start = Column(Date)
    date_program_start_actual = Column(Date)
    date_finalize_solicitation = Column(Date)
    date_finalize_solicitation_actual = Column(Date)
    date_accept_decline = Column(Date)
    date_accept_decline_actual = Column(Date)
    date_program_end = Column(Date)
    date_program_end_actual = Column(Date)
    date_release_rfp = Column(Date)
    date_proposal_analysis_1 = Column(Date)
    date_proposal_analysis_2 = Column(Date)
    date_responses_due = Column(Date)
    date_rebid_responses_due = Column(Date)
    default_currency_id = Column(BigInteger)
    default_distance_unit = Column(String(16))
    optional_py_spend = Column(Boolean)
    optional_py_room_nights = Column(Boolean)
    optional_fast_track = Column(Boolean)
    optional_hazard_country = Column(Boolean)
    optional_safety_score = Column(Boolean)
    rfp_scope = Column(Integer)
    rfp_targeted = Column(Integer, server_default=text("0"))
    count_solicited = Column(Integer, server_default=text("0"))
    count_accepted = Column(Integer, server_default=text("0"))
    count_negotiating = Column(Integer, server_default=text("0"))
    count_rejected = Column(Integer, server_default=text("0"))
    date_currency_conversion = Column(Date)
    last_smart_select = Column(TIMESTAMP(precision=6))
    last_client_share = Column(TIMESTAMP(precision=6))
    last_lanyon_send = Column(TIMESTAMP(precision=6))
    created = Column(TIMESTAMP(precision=6), server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), server_default=text("now()"))


class ProgramCurrency(Base):
    __tablename__ = 'program_currency'

    id = Column(BigInteger, primary_key=True)
    program_id = Column(ForeignKey('program.id'), nullable=False)
    currency_id = Column(BigInteger, nullable=False)
    currency_code = Column(String(8), nullable=False)
    currency_symbol = Column(String(8), nullable=False)
    conversion_date = Column(Date, nullable=False)
    conversion_rate = Column(Numeric(16, 8), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    program = relationship('Program')


class SortSet(Base):
    __tablename__ = 'sort_set'

    id = Column(BigInteger, primary_key=True)
    sort_clause = Column(String(256))
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    modified = Column(DateTime, nullable=False, server_default=text("now()"))


class ProgramHotel(Base):
    __tablename__ = 'program_hotel'

    id = Column(BigInteger, primary_key=True)
    program_id = Column(ForeignKey('program.id'), nullable=False)
    hotel_property_id = Column(ForeignKey('hotel_property.id'), nullable=False)
    hotel_master_id = Column(BigInteger)
    hotel_status = Column(String(16), nullable=False, server_default=text("'None'::character varying"))
    hotel_status_datetime = Column(TIMESTAMP(precision=6))
    dynamic_pricing_recommended = Column(Boolean, nullable=False, server_default=text("false"))
    spend_total_usd = Column(Numeric(16, 2))
    room_nights_total = Column(Integer)
    is_preferred = Column(Boolean)
    abr = Column(Numeric(16, 2))
    anr = Column(Numeric(16, 2))
    bar = Column(Numeric(16, 2))
    bcd = Column(Numeric(16, 2))
    olset_rating = Column(Integer)
    market_share = Column(Float(53))
    py_bid = Column(String(32))
    rate_availability = Column(Float(53))
    los_greater_than_5 = Column(Float(53))
    distance_closet_miles = Column(Float(53))
    anr_lanyon = Column(Numeric(16, 2))
    anr_lanyon_currency_code = Column(String(4))
    anr_dynamic = Column(Numeric(10, 0))
    consultant_recommendation = Column(String(32), server_default=text("'None'::character varying"))
    client_response = Column(String(16), nullable=False, server_default=text("'None'::character varying"))
    activity_count = Column(Integer, nullable=False, server_default=text("0"))
    count_consultant_comments = Column(Integer, server_default=text("0"))
    last_consultant_comment = Column(TIMESTAMP(precision=6))
    count_client_comments = Column(Integer, server_default=text("0"))
    last_client_comment = Column(TIMESTAMP(precision=6))
    count_free_comments = Column(Integer, server_default=text("0"))
    count_batch_comments = Column(Integer, server_default=text("0"))
    count_smartselect_comments = Column(Integer, server_default=text("0"))
    py_is_dynamic_pricing = Column(Boolean, server_default=text("false"))
    py_room_nights = Column(Integer)
    amenities_breakfast = Column(String(1))
    amenities_hsia = Column(String(1))
    amenities_wifi = Column(String(1))
    amenities_parking = Column(String(1))
    amenities_airporttx = Column(String(1))
    amenities_officetx = Column(String(1))
    amenities_fitness = Column(String(1))
    amenities_local_phone = Column(String(1))
    amenities_toll_phone = Column(String(1))
    fee_vatincluded = Column(String(1))
    fee_serviceincluded = Column(String(1))
    fee_lodgetaxincluded = Column(String(1))
    fee_statetaxincluded = Column(String(1))
    fee_citytaxincluded = Column(String(1))
    fee_occincluded = Column(String(1))
    fee_otherincluded = Column(String(1))
    pa_share_status = Column(String(16))
    count_pa_consultant_comments = Column(Integer, nullable=False, server_default=text("0"))
    count_pa_client_comments = Column(Integer, nullable=False, server_default=text("0"))
    count_pa_activity = Column(Integer, nullable=False, server_default=text("0"))
    count_pa_client_activity = Column(Integer, nullable=False, server_default=text("0"))
    bid_status = Column(String(32))
    bid_consultant_recommendation = Column(String(255))
    bid_client_recommendation = Column(String(255))
    bid_info = Column(String(64))
    bid_read_only = Column(Boolean, nullable=False, server_default=text("false"))
    is_reviewed_client = Column(Boolean, server_default=text("false"))
    is_reviewed_consultant = Column(Boolean, server_default=text("false"))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified_label = Column(String(255), server_default=text("''::character varying"))

    hotel_property = relationship('HotelProperty')
    program = relationship('Program')


class ProgramHotelActivity(Base):
    __tablename__ = 'program_hotel_activity'

    id = Column(BigInteger, primary_key=True)
    program_hotel_id = Column(ForeignKey('program_hotel.id'), nullable=False)
    advito_user_id = Column(BigInteger, nullable=False)
    advito_user_label = Column(String(64), nullable=False)
    activity_datetime = Column(TIMESTAMP(precision=6), nullable=False)
    activity_action = Column(String(32), nullable=False)
    action_value = Column(String(32))
    action_detail = Column(String(32))
    action_note = Column(Text)
    phase = Column(String(32), nullable=False, server_default=text("'Solicitiation'::character varying"))
    is_shared = Column(Boolean, nullable=False, server_default=text("false"))
    to_share_client = Column(Boolean, nullable=False, server_default=text("false"))
    to_share_hotel = Column(Boolean, nullable=False, server_default=text("false"))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    program_hotel = relationship('ProgramHotel')


class ProgramHotelBid(Base):
    __tablename__ = 'program_hotel_bid'

    id = Column(Integer, primary_key=True)
    lanyon_bid_id = Column(BigInteger, nullable=False)
    program_hotel_id = Column(ForeignKey('program_hotel.id'), nullable=False)
    bid_order = Column(Integer, nullable=False)
    bid_status = Column(String(32), nullable=False)
    bid_info = Column(String(32))
    consultant_recommendation = Column(Text)
    client_recommendation = Column(Text)
    is_shared = Column(Boolean)
    is_saved = Column(Boolean)
    property_overview = Column(Text)
    rate_type = Column(String(16))
    rate_currency = Column(String(8))
    rate = Column(Numeric(20, 2))
    rate_yoy_variance = Column(Float(53))
    rate_tcs = Column(Numeric(20, 2))
    dynamic_pricing = Column(CHAR(1))
    dynamic_percent_discount = Column(Integer)
    property_number_rooms = Column(Integer)
    room_nights = Column(Integer)
    room_type1_number = Column(Integer)
    room_inventory_percent = Column(Float(53))
    cancellation_policy = Column(String(16))
    amenities_breakfast = Column(String(1))
    amenities_breakfast_fee = Column(Numeric(10, 2))
    py_amenities_breakfast = Column(String(1))
    amenities_hsia = Column(String(1))
    amenities_hsia_fee = Column(Numeric(10, 2))
    py_amenities_hsia = Column(String(1))
    amenities_wifi = Column(String(1))
    amenities_wifi_fee = Column(Numeric(10, 2))
    py_amenities_wifi = Column(String(1))
    amenities_parking = Column(String(1))
    amenities_parking_fee = Column(Numeric(10, 2))
    py_amenities_parking = Column(String(1))
    amenities_airporttx = Column(String(1))
    amenities_airporttx_fee = Column(Numeric(10, 2))
    py_amenities_airporttx = Column(String(1))
    amenities_officetx = Column(String(1))
    amenities_officetx_fee = Column(Numeric(10, 2))
    py_amenities_officetx = Column(String(1))
    amenities_fitness = Column(String(1))
    amenities_fitness_fee = Column(Numeric(10, 2))
    py_amenities_fitness = Column(String(1))
    amenities_localphone = Column(String(1))
    amenities_localphone_fee = Column(Numeric(10, 2))
    py_amenities_localphone = Column(String(1))
    amenities_tollphone = Column(String(1))
    amenities_tollphone_fee = Column(Numeric(10, 2))
    py_amenities_tollphone = Column(String(1))
    bid_comments = Column(Text)
    fee_vat = Column(Numeric(10, 2))
    fee_vat_uom = Column(String(1))
    fee_vat_included = Column(String(1))
    py_fee_vat_included = Column(String(1))
    fee_vatfb = Column(Numeric(10, 2))
    fee_vatfb_uom = Column(String(1))
    fee_vatfb_included = Column(String(1))
    py_fee_vatfb_included = Column(String(1))
    fee_service = Column(Numeric(10, 2))
    fee_service_uom = Column(String(1))
    fee_service_included = Column(String(1))
    py_fee_service_included = Column(String(1))
    fee_lodgetax = Column(Numeric(10, 2))
    fee_lodgetax_uom = Column(String(1))
    fee_lodgetax_included = Column(String(1))
    py_fee_lodgetax_included = Column(String(1))
    fee_statetax = Column(Numeric(10, 2))
    fee_statetax_uom = Column(String(1))
    fee_statetax_included = Column(String(1))
    py_fee_statetax_included = Column(String(1))
    fee_citytax = Column(Numeric(10, 2))
    fee_citytax_uom = Column(String(1))
    fee_citytax_included = Column(String(1))
    py_fee_citytax_included = Column(String(1))
    fee_occ = Column(Numeric(10, 2))
    fee_occ_uom = Column(String(1))
    fee_occ_included = Column(String(1))
    py_fee_occ_included = Column(String(1))
    fee_other = Column(Numeric(10, 2))
    fee_other_uom = Column(String(1))
    fee_other_description = Column(Text)
    fee_other_included = Column(String(1))
    py_fee_other_included = Column(String(1))
    count_seasons = Column(Integer)
    season_1_start = Column(Date)
    season_1_end = Column(Date)
    lra_s1_rt1_sgl = Column(Numeric(20, 2))
    lra_s1_rt1_dbl = Column(Numeric(20, 2))
    lra_s1_rt2_sgl = Column(Numeric(20, 2))
    lra_s1_rt2_dbl = Column(Numeric(20, 2))
    lra_s1_rt3_sgl = Column(Numeric(20, 2))
    lra_s1_rt3_dbl = Column(Numeric(20, 2))
    nlra_s1_rt1_sgl = Column(Numeric(20, 2))
    nlra_s1_rt1_dbl = Column(Numeric(20, 2))
    nlra_s1_rt2_sgl = Column(Numeric(20, 2))
    nlra_s1_rt2_dbl = Column(Numeric(20, 2))
    nlra_s1_rt3_sgl = Column(Numeric(20, 2))
    nlra_s1_rt3_dbl = Column(Numeric(20, 2))
    govt_s1_rt1_sgl = Column(Numeric(20, 2))
    govt_s1_rt1_dbl = Column(Numeric(20, 2))
    govt_s1_rt2_sgl = Column(Numeric(20, 2))
    govt_s1_rt2_dbl = Column(Numeric(20, 2))
    govt_s1_rt3_sgl = Column(Numeric(20, 2))
    govt_s1_rt3_dbl = Column(Numeric(20, 2))
    season_2_start = Column(Date)
    season_2_end = Column(Date)
    lra_s2_rt1_sgl = Column(Numeric(20, 2))
    lra_s2_rt1_dbl = Column(Numeric(20, 2))
    lra_s2_rt2_sgl = Column(Numeric(20, 2))
    lra_s2_rt2_dbl = Column(Numeric(20, 2))
    lra_s2_rt3_sgl = Column(Numeric(20, 2))
    lra_s2_rt3_dbl = Column(Numeric(20, 2))
    nlra_s2_rt1_sgl = Column(Numeric(20, 2))
    nlra_s2_rt1_dbl = Column(Numeric(20, 2))
    nlra_s2_rt2_sgl = Column(Numeric(20, 2))
    nlra_s2_rt2_dbl = Column(Numeric(20, 2))
    nlra_s2_rt3_sgl = Column(Numeric(20, 2))
    nlra_s2_rt3_dbl = Column(Numeric(20, 2))
    govt_s2_rt1_sgl = Column(Numeric(20, 2))
    govt_s2_rt1_dbl = Column(Numeric(20, 2))
    govt_s2_rt2_sgl = Column(Numeric(20, 2))
    govt_s2_rt2_dbl = Column(Numeric(20, 2))
    govt_s2_rt3_sgl = Column(Numeric(20, 2))
    govt_s2_rt3_dbl = Column(Numeric(20, 2))
    season_3_start = Column(Date)
    season_3_end = Column(Date)
    lra_s3_rt1_sgl = Column(Numeric(20, 2))
    lra_s3_rt1_dbl = Column(Numeric(20, 2))
    lra_s3_rt2_sgl = Column(Numeric(20, 2))
    lra_s3_rt2_dbl = Column(Numeric(20, 2))
    lra_s3_rt3_sgl = Column(Numeric(20, 2))
    lra_s3_rt3_dbl = Column(Numeric(20, 2))
    nlra_s3_rt1_sgl = Column(Numeric(20, 2))
    nlra_s3_rt1_dbl = Column(Numeric(20, 2))
    nlra_s3_rt2_sgl = Column(Numeric(20, 2))
    nlra_s3_rt2_dbl = Column(Numeric(20, 2))
    nlra_s3_rt3_sgl = Column(Numeric(20, 2))
    nlra_s3_rt3_dbl = Column(Numeric(20, 2))
    govt_s3_rt1_sgl = Column(Numeric(20, 2))
    govt_s3_rt1_dbl = Column(Numeric(20, 2))
    govt_s3_rt2_sgl = Column(Numeric(20, 2))
    govt_s3_rt2_dbl = Column(Numeric(20, 2))
    govt_s3_rt3_sgl = Column(Numeric(20, 2))
    govt_s3_rt3_dbl = Column(Numeric(20, 2))
    season_4_start = Column(Date)
    season_4_end = Column(Date)
    lra_s4_rt1_sgl = Column(Numeric(20, 2))
    lra_s4_rt1_dbl = Column(Numeric(20, 2))
    lra_s4_rt2_sgl = Column(Numeric(20, 2))
    lra_s4_rt2_dbl = Column(Numeric(20, 2))
    lra_s4_rt3_sgl = Column(Numeric(20, 2))
    lra_s4_rt3_dbl = Column(Numeric(20, 2))
    nlra_s4_rt1_sgl = Column(Numeric(20, 2))
    nlra_s4_rt1_dbl = Column(Numeric(20, 2))
    nlra_s4_rt2_sgl = Column(Numeric(20, 2))
    nlra_s4_rt2_dbl = Column(Numeric(20, 2))
    nlra_s4_rt3_sgl = Column(Numeric(20, 2))
    nlra_s4_rt3_dbl = Column(Numeric(20, 2))
    govt_s4_rt1_sgl = Column(Numeric(20, 2))
    govt_s4_rt1_dbl = Column(Numeric(20, 2))
    govt_s4_rt2_sgl = Column(Numeric(20, 2))
    govt_s4_rt2_dbl = Column(Numeric(20, 2))
    govt_s4_rt3_sgl = Column(Numeric(20, 2))
    govt_s4_rt3_dbl = Column(Numeric(20, 2))
    season_5_start = Column(Date)
    season_5_end = Column(Date)
    lra_s5_rt1_sgl = Column(Numeric(20, 2))
    lra_s5_rt1_dbl = Column(Numeric(20, 2))
    lra_s5_rt2_sgl = Column(Numeric(20, 2))
    lra_s5_rt2_dbl = Column(Numeric(20, 2))
    lra_s5_rt3_sgl = Column(Numeric(20, 2))
    lra_s5_rt3_dbl = Column(Numeric(20, 2))
    nlra_s5_rt1_sgl = Column(Numeric(20, 2))
    nlra_s5_rt1_dbl = Column(Numeric(20, 2))
    nlra_s5_rt2_sgl = Column(Numeric(20, 2))
    nlra_s5_rt2_dbl = Column(Numeric(20, 2))
    nlra_s5_rt3_sgl = Column(Numeric(20, 2))
    nlra_s5_rt3_dbl = Column(Numeric(20, 2))
    govt_s5_rt1_sgl = Column(Numeric(20, 2))
    govt_s5_rt1_dbl = Column(Numeric(20, 2))
    govt_s5_rt2_sgl = Column(Numeric(20, 2))
    govt_s5_rt2_dbl = Column(Numeric(20, 2))
    govt_s5_rt3_sgl = Column(Numeric(20, 2))
    govt_s5_rt3_dbl = Column(Numeric(20, 2))
    count_blackouts = Column(Integer)
    blackout_1_start_date = Column(Date)
    blackout_1_end_date = Column(Date)
    blackout_1_name = Column(String(64))
    blackout_2_start_date = Column(Date)
    blackout_2_end_date = Column(Date)
    blackout_2_name = Column(String(64))
    blackout_3_start_date = Column(Date)
    blackout_3_end_date = Column(Date)
    blackout_3_name = Column(String(64))
    blackout_4_start_date = Column(Date)
    blackout_4_end_date = Column(Date)
    blackout_4_name = Column(String(64))
    blackout_5_start_date = Column(Date)
    blackout_5_end_date = Column(Date)
    blackout_5_name = Column(String(64))
    blackout_6_start_date = Column(Date)
    blackout_6_end_date = Column(Date)
    blackout_6_name = Column(String(64))
    blackout_7_start_date = Column(Date)
    blackout_7_end_date = Column(Date)
    blackout_7_name = Column(String(64))
    blackout_8_start_date = Column(Date)
    blackout_8_end_date = Column(Date)
    blackout_8_name = Column(String(64))
    bar_rate_discount = Column(Numeric(20, 2))
    offered_lra = Column(Numeric(20, 2))
    py_lra = Column(Numeric(20, 2))
    yoy_lra_percent_change = Column(Float(53))
    offered_nlra = Column(Numeric(20, 2))
    py_nlra = Column(Numeric(20, 2))
    yoy_nlra_percent_change = Column(Float(53))
    requested_adr_round_1 = Column(Numeric(20, 2))
    overall_score = Column(Float(53))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    program_hotel = relationship('ProgramHotel')


class ProgramMarket(Base):
    __tablename__ = 'program_market'

    id = Column(BigInteger, primary_key=True)
    program_id = Column(ForeignKey('program.id'), nullable=False)
    geo_city_id = Column(BigInteger, nullable=False, index=True)
    market_property_count = Column(Integer)
    market_spend = Column(Numeric(16, 2))
    market_room_nights = Column(Integer)
    market_room_nights_py = Column(Integer)
    market_room_nights_compliance = Column(Float)
    market_abr = Column(Numeric(16, 2))
    market_anr = Column(Numeric(16, 2))
    market_bar = Column(Numeric(16, 2))
    market_preferred_hotels = Column(Integer)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    client_metro_area_id = Column(BigInteger)
    market_bcd = Column(Numeric(16, 2))

    program = relationship('Program')


class ProgramSetting(Base):
    __tablename__ = 'program_settings'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('program_settings_id_seq'::regclass)"))
    program_id = Column(ForeignKey('program.id'), nullable=False)
    preferred_yoy_increase = Column(Integer)
    number_nights_no_yoy = Column(Integer)
    number_nights_1 = Column(Integer)
    number_nights_percentage_1 = Column(Integer)
    number_nights_2 = Column(Integer)
    number_nights_percentage_2 = Column(Integer)
    number_nights_3 = Column(Integer)
    number_nights_percentage_3 = Column(Integer)
    number_nights_threshold = Column(Integer)
    inventory_number_1 = Column(Integer)
    inventory_percentage_1 = Column(Integer)
    inventory_number_2 = Column(Integer)
    inventory_percentage_2 = Column(Integer)
    inventory_number_3 = Column(Integer)
    inventory_percentage_3 = Column(Integer)
    amenities_breakfast = Column(Boolean)
    amenities_parking = Column(Boolean)
    amenities_fitness = Column(Boolean)
    amenities_wifi = Column(Boolean)
    amenities_hsia = Column(Boolean)
    amenities_airport = Column(Boolean)
    amenities_office_tx = Column(Boolean)
    amenities_phone = Column(Boolean)
    amenities_toll = Column(Boolean)
    fee_vat = Column(Boolean)
    fee_service = Column(Boolean)
    fee_lodge = Column(Boolean)
    fee_tax_city = Column(Boolean)
    fee_tax_state = Column(Boolean)
    fee_occ = Column(Boolean)
    fee_vat_fb = Column(Boolean)
    created = Column(TIMESTAMP(precision=6), server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), server_default=text("now()"))

    program = relationship('Program')

    def serialize(self):
        return {
            'id': self.id,
            'clientProgramId': self.program_id,
            'preferredYoyIncrease': ('Allow Increase YOY'
                                     if self.preferred_yoy_increase
                                     else 'No Increase YOY'),
            'numberNightsNoYoy': self.number_nights_no_yoy,
            'numberNights1': self.number_nights_1,
            'numberNightsPercentage1': '{}%'.format(self.number_nights_percentage_1),
            'numberNights2': self.number_nights_2,
            'numberNightsPercentage2': '{}%'.format(self.number_nights_percentage_2),
            'numberNightsThreshold': self.number_nights_threshold,
            'inventoryNumber1': self.inventory_number_1,
            'inventoryPercentage1': '{}%'.format(self.inventory_percentage_1),
            'inventoryNumber2': self.inventory_number_2,
            'inventoryPercentage2': '{}%'.format(self.inventory_percentage_2),
            'inventoryNumber3': self.inventory_number_3,
            'inventoryPercentage3': '{}%'.format(self.inventory_percentage_3),
            'breakfast': self.amenities_breakfast,
            'parking': self.amenities_parking,
            'fitness': self.amenities_fitness,
            'wifi': self.amenities_wifi,
            'hsia': self.amenities_hsia,
            'airport': self.amenities_airport,
            'office': self.amenities_office_tx,
            'localPhone': self.amenities_phone,
            'tollCalls': self.amenities_toll,
            'feeVat': self.fee_vat,
            'feeService': self.fee_service,
            'feeLodge': self.fee_lodge,
            'feeCityTax': self.fee_tax_city,
            'feeStateTax': self.fee_tax_state,
            'feeOcc': self.fee_occ,
            'feeVatFb': self.fee_vat_fb
        }

    def deserialize(self, data):
        self.preferred_yoy_increase = data.get('PreferredYoyIncrease')
        self.number_nights_no_yoy = data.get('NumberNightsNoYoy')
        self.number_nights_1 = data.get('NumberNights1')
        self.number_nights_percentage_1 = data.get('NumberNightsPercentage1')
        self.number_nights_2 = data.get('NumberNights2')
        self.number_nights_percentage_2 = data.get('NumberNightsPercentage2')
        # self.number_nights_3 = data['NumberNights3']
        # self.number_nights_percentage_3 = data.get('NumberNightsPercentage3')
        self.number_nights_threshold = data.get('NumberNightsThreshold')
        self.inventory_number_1 = data.get('InventoryNumber1')
        self.inventory_percentage_1 = data.get('InventoryPercentage1')
        self.inventory_number_2 = data.get('InventoryNumber2')
        self.inventory_percentage_2 = data.get('InventoryPercentage2')
        self.inventory_number_3 = data.get('InventoryNumber3')
        self.inventory_percentage_3 = data.get('InventoryPercentage3')
        self.amenities_breakfast = data.get('breakfast')
        self.amenities_parking = data.get('parking')
        self.amenities_fitness = data.get('fitness')
        self.amenities_wifi = data.get('wifi')
        self.amenities_hsia = data.get('hsia')
        self.amenities_airport = data.get('airport')
        self.amenities_office_tx = data.get('office')
        self.amenities_phone = data.get('localPhone')
        self.amenities_toll = data.get('tollCalls')
        self.fee_vat = data.get('FeeVat')
        self.fee_service = data.get('FeeService')
        self.fee_lodge = data.get('FeeLodge')
        self.fee_tax_city = data.get('FeeCityTax')
        self.fee_tax_state = data.get('FeeStateTax')
        self.fee_occ = data.get('FeeOcc')
        self.fee_vat_fb = data.get('FeeVatFb')
        self.modified = datetime.now()


class SmartselectRule(Base):
    __tablename__ = 'smartselect_rule'

    id = Column(BigInteger, primary_key=True)
    program_id = Column(ForeignKey('program.id'), nullable=False)
    smartselect_rule_type_id = Column(ForeignKey('smartselect_rule_type.id'), nullable=False)
    rule_action = Column(String(32), nullable=False)
    rule_value_1 = Column(String(255), nullable=False)
    rule_select_1 = Column(String(64), nullable=False)
    rule_value_2 = Column(String(255))
    rule_select_2 = Column(String(64))
    rule_comment = Column(Text)
    is_applied = Column(Boolean, nullable=False, server_default=text("false"))
    last_applied_datetime = Column(DateTime)
    option_1 = Column(String(64), server_default=text("now()"))
    option_2 = Column(String(64))
    geo_region_id = Column(BigInteger)
    geo_country_id = Column(BigInteger)
    geo_state_id = Column(BigInteger)
    geo_city_id = Column(BigInteger)
    metro_area_id = Column(BigInteger)
    region_label = Column(String(128))
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    modified = Column(DateTime, nullable=False, server_default=text("now()"))

    program = relationship('Program')
    smartselect_rule_type = relationship('SmartselectRuleType')

    def serialize(self):
        description = ''
        rule_type = self.smartselect_rule_type
        if rule_type:
            description = self.smartselect_rule_type.label_1
            description = (
                '{} {}'.format(description, self.smartselect_rule_type.label_2)
                if self.smartselect_rule_type.label_2
                else description
            )
            description = description.replace(
                '[[VALUE1]]', self.rule_value_1 if self.rule_value_1 else '')
            description = description.replace(
                '[[VALUE2]]', self.rule_value_2 if self.rule_value_2 else '')
            description = description.replace(
                '[[SELECT1]]', self.rule_select_1 if self.rule_select_1 else '')
            description = description.replace(
                '[[SELECT2]]', self.rule_select_2 if self.rule_select_2 else '')
            description = description.replace(
                '[[OPTION1]]', self.option_1 if self.option_1 else '')
            description = description.replace(
                '[[OPTION2]]', self.option_2 if self.option_2 else '')
        return {
            'smartSelectRuleId': self.id,
            'ruleType': self.smartselect_rule_type.rule_type_name,
            'ruleDescription': description,
            # 'ruleDescription': (
            #     'In markets with volume of at least {} {} {}'.format(
            #         self.option_1, self.rule_value_1, self.rule_select_1)),
            'regionLabel': self.region_label,
            'comment': self.rule_comment,
            'created': datetime.strftime(self.created, '%d %b %Y'),
        }


class SmartselectRuleType(Base):
    __tablename__ = 'smartselect_rule_type'

    id = Column(BigInteger, primary_key=True)
    rule_type_name = Column(String(64), nullable=False)
    rule_type_note = Column(Text)
    column_1 = Column(String(64), nullable=False)
    select_1 = Column(String(64), nullable=False)
    operator_1 = Column(String(16), nullable=False)
    label_1 = Column(String(128), nullable=False)
    column_2 = Column(String(64))
    select_2 = Column(String(64))
    operator_2 = Column(String(16))
    label_2 = Column(String(128))
    base_action = Column(String(16), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
