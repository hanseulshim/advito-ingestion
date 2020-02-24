# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, JSON, Numeric, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AdvitoApplication(Base):
    __tablename__ = 'advito_application'

    id = Column(BigInteger, primary_key=True)
    application_name = Column(String(32), nullable=False)
    application_full = Column(String(64), nullable=False)
    application_tag = Column(String(8), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    description = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class AdvitoGroup(Base):
    __tablename__ = 'advito_group'

    id = Column(BigInteger, primary_key=True)
    group_name = Column(String(64), nullable=False)
    group_tag = Column(String(8))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    description = Column(Text)
    is_assignable = Column(Boolean, nullable=False, server_default=text("true"))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class Airport(Base):
    __tablename__ = 'airport'

    id = Column(BigInteger, primary_key=True)
    airport_name = Column(String(64), nullable=False)
    airport_code = Column(String(8), nullable=False)
    airport_type = Column(String(32))
    address1 = Column(String(64))
    address2 = Column(String(64))
    postal_code = Column(String(16))
    geo_city_id = Column(BigInteger)
    geo_country_id = Column(BigInteger)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    modified = Column(DateTime, nullable=False, server_default=text("now()"))


class Alert(Base):
    __tablename__ = 'alert'

    id = Column(BigInteger, primary_key=True)
    application_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger)
    role_id = Column(BigInteger)
    client_id = Column(BigInteger)
    alert_status = Column(String(32), nullable=False, server_default=text("'Active'::character varying"))
    alert_type = Column(String(32), nullable=False)
    alert_timestamp = Column(DateTime, nullable=False)
    alert_expiration_timestamp = Column(DateTime)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    alert_text = Column(String(256), nullable=False)
    alert_detail = Column(String(256))
    alert_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


t_allergan_regions = Table(
    'allergan_regions', metadata,
    Column('Region*', String(255)),
    Column('Country*', String(255))
)


class BcdGeoContinent(Base):
    __tablename__ = 'bcd_geo_continent'

    id = Column(BigInteger, primary_key=True)
    continent_name = Column(String(32), nullable=False, unique=True)
    continent_tag = Column(String(8), nullable=False)
    continent_code = Column(String(4), nullable=False, unique=True)
    note = Column(Text)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class BcdGeoRegionGroup(Base):
    __tablename__ = 'bcd_geo_region_group'

    id = Column(BigInteger, primary_key=True)
    region_group_name = Column(String(32), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class ClientApprovalStatu(Base):
    __tablename__ = 'client_approval_status'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_approval_status_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class ClientExpType(Base):
    __tablename__ = 'client_exp_type'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_exp_type_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class ClientPymtStatu(Base):
    __tablename__ = 'client_pymt_status'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_pymt_status_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class ClientPymtType(Base):
    __tablename__ = 'client_pymt_type'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_pymt_type_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class ClientReceiptType(Base):
    __tablename__ = 'client_receipt_type'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_receipt_type_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class ClientTravelJournal(Base):
    __tablename__ = 'client_travel_journal'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_travel_journal_id_seq'::regclass)"))
    emp_cp_code = Column(BigInteger)
    biz_area = Column(String(255))
    emp_cost_cntr = Column(String(255))
    emp_cost_cntr_id = Column(BigInteger)
    rpt_cp_code = Column(BigInteger)
    rpt_cost_cntr = Column(String(255))
    rpt_cost_cntr_id = Column(BigInteger)
    entry_cost_cntr = Column(String(255))
    entry_cost_cntr_id = Column(BigInteger)
    exp_policy = Column(String(255))
    exp_policy_id = Column(BigInteger)
    entry_trns_date = Column(DateTime)
    parnt_exp_type = Column(String(255))
    parnt_exp_type_id = Column(BigInteger)
    exp_type = Column(String(255))
    exp_type_id = Column(BigInteger)
    trns_typ = Column(String(255))
    trns_typ_id = Column(BigInteger)
    entr_descript = Column(Text)
    vendor = Column(String(255))
    vendor_id = Column(BigInteger)
    pymt_status = Column(String(255))
    pymt_status_id = Column(BigInteger)
    trns_amt = Column(Float, server_default=text("0"))
    trns_currency = Column(String(255))
    trns_curr_id = Column(BigInteger)
    posted_amount = Column(Float, server_default=text("0"))
    posted_currency = Column(String(255))
    posted_currency_id = Column(BigInteger)
    f17_budget_rates = Column(Float, server_default=text("0"))
    f17_amount_in_gbp = Column(Float, server_default=text("0"))
    exchange_rate = Column(Float, server_default=text("0"))
    receipt_type = Column(String(255))
    receipt_type_id = Column(BigInteger)
    ispersonal = Column(Boolean)
    loc_from = Column(String(255))
    loc_from_country_id = Column(BigInteger)
    loc_from_city_id = Column(BigInteger)
    loc_to = Column(String(255))
    loc_to_country_id = Column(BigInteger)
    loc_to_city_id = Column(BigInteger)
    noattendee = Column(Integer)
    isapproved = Column(Boolean)
    approvalstatus = Column(BigInteger)
    country_id = Column(BigInteger)
    city_id = Column(BigInteger)
    gl_code = Column(BigInteger)
    anp_exps_type = Column(String(255))
    anp_gl_code = Column(String(255))
    country_code = Column(String(255))
    sap_internal_order = Column(String(255))
    wbs_element = Column(String(255))
    last_submitted_date = Column(DateTime)
    sent_for_pymt_date = Column(DateTime)
    isreceptsreceived = Column(Boolean)
    isreceptimage = Column(Boolean)
    isreceiptimgreq = Column(Boolean)
    isreceiptreq = Column(Boolean)
    pymttype = Column(String(255))
    pymttype_id = Column(BigInteger)
    refnum = Column(String(255))
    entrylegacykey = Column(String(255))
    rptkey = Column(String(255))
    extracteddate = Column(DateTime)
    creationdate = Column(DateTime)
    firstapproveddate = Column(DateTime)
    parententrykey = Column(String(255))
    profitcenter = Column(String(255))
    profit_cntr_id = Column(BigInteger)
    region_id = Column(BigInteger)
    market_id = Column(BigInteger)
    business = Column(String(255))
    ageing = Column(Float, server_default=text("0"))
    iscompliant = Column(Boolean)
    marketl1 = Column(String(255))
    marketl1_id = Column(BigInteger)
    marketl3 = Column(String(255))
    marketl3_id = Column(BigInteger)
    countryl1 = Column(String(255))
    period = Column(String(255))
    imp_date = Column(DateTime)
    imp_source = Column(String(255))
    imp_source_linenum = Column(String(255))
    country_val = Column(String(255))
    location_val = Column(String(255))
    region_val = Column(String(255))
    market_val = Column(String(255))
    ispersonal_val = Column(String(32))
    isreceiptreq_val = Column(String(32))
    isreceiptimgreq_val = Column(String(32))
    isreceptimage_val = Column(String(32))
    isreceptsreceived_val = Column(String(32))
    iscompliant_val = Column(String(32))
    approvalstatus_val = Column(String(255))
    ageing_val = Column(String(32))


class ClientTrnsTyp(Base):
    __tablename__ = 'client_trns_typ'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_trns_typ_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class ClientVendor(Base):
    __tablename__ = 'client_vendor'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('client_vendor_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class ClientprofitCntr(Base):
    __tablename__ = 'clientprofit_cntr'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('clientprofit_cntr_id_seq'::regclass)"))
    name_value = Column(String(255), nullable=False)


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(BigInteger, primary_key=True)
    currency_name = Column(String(64), nullable=False)
    currency_code = Column(String(4), nullable=False)
    currency_symbol = Column(String(4))
    currency_priority = Column(Integer)
    currency_flag_icon = Column(String(32))
    currency_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class CurrencyConversion(Base):
    __tablename__ = 'currency_conversion'

    id = Column(BigInteger, primary_key=True)
    conversion_date = Column(Date, nullable=False, index=True)
    currency_code_from = Column(String(8), index=True)
    currency_code_to = Column(String(8), nullable=False, index=True)
    conversion_rate = Column(Numeric(16, 8), nullable=False)
    conversion_rate_reverse = Column(Numeric(16, 8))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


t_dbimp_client_auto = Table(
    'dbimp_client_auto', metadata,
    Column('id', BigInteger),
    Column('client_name', String(128)),
    Column('client_name_full', String(64)),
    Column('client_tag', String(8)),
    Column('client_code', String(128)),
    Column('lanyon_client_code', String(16)),
    Column('gcn', String(16)),
    Column('is_active', Boolean, nullable=False, server_default=text("true")),
    Column('logo_path', String(128)),
    Column('description', Text),
    Column('industry', String(64)),
    Column('default_currency_code', String(8)),
    Column('default_distance_units', String(132)),
    Column('geo_region_group_id', BigInteger),
    Column('created', TIMESTAMP(precision=6), nullable=False, server_default=text("now()")),
    Column('modified', TIMESTAMP(precision=6), nullable=False, server_default=text("now()")),
    Column('lockreadonly', Boolean),
    Column('sourcetable', String(255)),
    Column('isgovernmentcontractor', Boolean),
    Column('mostrecentspend', String(255)),
    Column('primaryemail', String(255))
)


class GeoCountry(Base):
    __tablename__ = 'geo_country'

    id = Column(BigInteger, primary_key=True)
    geo_continent_id = Column(BigInteger)
    country_name = Column(String(64), nullable=False)
    country_code_2char = Column(String(4), nullable=False)
    country_code_3char = Column(String(4))
    country_code_numeric = Column(String(4))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    default_currency_code = Column(String(4))
    state_label = Column(String(64))
    master_created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    master_modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    note = Column(Text)
    is_required_in_regions = Column(Boolean, nullable=False, server_default=text("true"))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class GeoRegion(Base):
    __tablename__ = 'geo_region'

    id = Column(BigInteger, primary_key=True)
    geo_region_group_id = Column(BigInteger, nullable=False)
    region_name = Column(String(64), nullable=False)
    region_code = Column(String(4))
    region_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class GeoRegionGroup(Base):
    __tablename__ = 'geo_region_group'

    id = Column(BigInteger, primary_key=True)
    region_group_name = Column(String(32), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


class ReasonCodeGlobal(Base):
    __tablename__ = 'reason_code_global'
    __table_args__ = (
        UniqueConstraint('code_type', 'reason_code_global'),
    )

    id = Column(BigInteger, primary_key=True)
    code_type = Column(String(16), nullable=False)
    reason_code_global = Column(String(8), nullable=False)
    code_description = Column(String(64), nullable=False)
    note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))


t_temp_import_agency = Table(
    'temp_import_agency', metadata,
    Column('product_type', String(255)),
    Column('client_name', String(255)),
    Column('record_key', String(255)),
    Column('global_customer_number', String(255)),
    Column('client_code', String(255)),
    Column('locator', String(255)),
    Column('traveler', String(255)),
    Column('invoice_date', String(255)),
    Column('invoice_number', String(255)),
    Column('agency', String(255)),
    Column('agency_number', String(255)),
    Column('booking_source', String(255)),
    Column('booking_agent_id', String(255)),
    Column('local_reason_code', String(255)),
    Column('local_reason_code_description', String(255)),
    Column('global_reason_code', String(255)),
    Column('global_reason_code_description', String(255)),
    Column('ratetype_code', String(255)),
    Column('rate_type_description', String(255)),
    Column('refund_indicator', String(255)),
    Column('exchange_indicator', String(255)),
    Column('credit_card_number', String(255)),
    Column('credit_card_type', String(255)),
    Column('credit_card_expiration', String(255)),
    Column('traveler_country', String(255)),
    Column('ticketing_country', String(255)),
    Column('int_dom', String(255)),
    Column('travel_sector', String(255)),
    Column('regional_indicator', String(255)),
    Column('round_trip_indicator', String(255)),
    Column('shortlong_haul_indicator', String(255)),
    Column('mileage', String(255)),
    Column('original_document_number', String(255)),
    Column('ticket_confirmation_number', String(255)),
    Column('net_count', String(255)),
    Column('travel_start_date', String(255)),
    Column('trip_length', String(255)),
    Column('days_advance_purchase', String(255)),
    Column('days_advance_purchase_group', String(255)),
    Column('origin_city', String(255)),
    Column('destination_city', String(255)),
    Column('vendor', String(255)),
    Column('service_description', String(255)),
    Column('service_category', String(255)),
    Column('daily_rate_minus_tax_usd', String(255)),
    Column('tax_amount_usd', String(255)),
    Column('total_invoice_amount_usd', String(255)),
    Column('low_fare_usd', String(255)),
    Column('full_fare_usd', String(255)),
    Column('fare_before_discount_usd', String(255)),
    Column('amount_lost_usd', String(255)),
    Column('full_fare_savings_usd', String(255)),
    Column('contract_savings_usd', String(255)),
    Column('cost_center', String(255)),
    Column('department', String(255)),
    Column('employee_id', String(255)),
    Column('employee_level', String(255)),
    Column('line_of_business', String(255)),
    Column('subline_of_business', String(255))
)


class TempImportAirport(Base):
    __tablename__ = 'temp_import_airport'

    airport_code = Column(String(255))
    airport_name = Column(String(255))
    airport_address = Column(String(255))
    latitude = Column(String(255))
    longitude = Column(String(255))
    airport_name2 = Column(String(255))
    airport_type = Column(String(255))
    city_code = Column(String(255))
    city_name = Column(String(255))
    state_code = Column(String(255))
    state_name = Column(String(255))
    country_code = Column(String(255))
    country_name = Column(String(255))
    subregion_code = Column(String(255))
    subregion_name = Column(String(255))
    subregion_name_short = Column(String(255))
    region_code = Column(String(255))
    region_name = Column(String(255))
    id = Column(String(255), primary_key=True)


t_temp_import_reason_codes = Table(
    'temp_import_reason_codes', metadata,
    Column('agency', String(255)),
    Column('agency_number', String(255)),
    Column('booking_source', String(255)),
    Column('booking_agent_id', String(255)),
    Column('local_reason_code', String(255)),
    Column('local_reason_code_desc', String(255)),
    Column('global_reason_code', String(255)),
    Column('global_reason_code_desc', String(255))
)


class TempStoryAir01Barchart(Base):
    __tablename__ = 'temp_story_air01_barchart'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)


t_temp_story_air01_barchart_data = Table(
    'temp_story_air01_barchart_data', metadata,
    Column('barchartid', BigInteger),
    Column('category', String(255)),
    Column('value', Integer),
    Column('change', String(255))
)


class TempStoryAir01Kpi(Base):
    __tablename__ = 'temp_story_air01_kpi'

    title = Column(String(255), primary_key=True)
    kpi_value = Column(Integer)
    delta = Column(Float)
    change = Column(String(255))
    kpi_type = Column(String(255))
    icon = Column(String(255))
    percent = Column(Float)


class TempStoryAir01Location(Base):
    __tablename__ = 'temp_story_air01_location'

    id = Column(BigInteger, primary_key=True)
    thickness = Column(Integer)
    height = Column(Float)
    opacity = Column(Float)
    _from = Column('from', String(255))
    to = Column(String(255))


class TempStoryAir01LocationCoord(Base):
    __tablename__ = 'temp_story_air01_location_coord'

    id = Column(BigInteger, primary_key=True)
    locationid = Column(BigInteger, nullable=False)
    latitude = Column(Numeric(10, 7), nullable=False)
    longitude = Column(Numeric(10, 7), nullable=False)


class TempStoryAir02Bar(Base):
    __tablename__ = 'temp_story_air02_bar'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    type = Column(String(255))


class TempStoryAir02BarDatum(Base):
    __tablename__ = 'temp_story_air02_bar_data'

    id = Column(BigInteger, primary_key=True)
    barid = Column(BigInteger)
    category = Column(String(255))
    value = Column(Integer)
    change = Column(String(255))


class TempStoryAir02Kpi(Base):
    __tablename__ = 'temp_story_air02_kpi'

    title = Column(String(255), primary_key=True)
    value = Column(Integer)
    delta = Column(Integer)
    change = Column(String(255))
    type = Column(String(255))
    icon = Column(String(255))
    percent = Column(Float)


class TempStoryAir02Location(Base):
    __tablename__ = 'temp_story_air02_location'

    id = Column(BigInteger, primary_key=True)
    thickness = Column(Integer)
    height = Column(Float)
    opacity = Column(Float)
    _from = Column('from', String(255))
    to = Column(String(255))


class TempStoryAir02LocationCoord(Base):
    __tablename__ = 'temp_story_air02_location_coord'

    id = Column(BigInteger, primary_key=True)
    locationid = Column(BigInteger, nullable=False)
    latitude = Column(Numeric(10, 7), nullable=False)
    longitude = Column(Numeric(10, 7), nullable=False)


class TempStoryAir03Category(Base):
    __tablename__ = 'temp_story_air03_category'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    icon = Column(String(255))
    total = Column(Integer)


class TempStoryAir03Subcategory(Base):
    __tablename__ = 'temp_story_air03_subcategory'

    id = Column(BigInteger, primary_key=True)
    categoryid = Column(BigInteger)
    name = Column(String(255))
    value = Column(String(255))
    delta = Column(String(255))
    color = Column(String(255))
    percent = Column(Float)


class TempStoryAir04Bar(Base):
    __tablename__ = 'temp_story_air04_bar'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    type = Column(String(255))


class TempStoryAir04BarDatum(Base):
    __tablename__ = 'temp_story_air04_bar_data'

    id = Column(BigInteger, primary_key=True)
    barid = Column(BigInteger)
    category = Column(String(255))
    change = Column(String(255))
    value = Column(Integer)


class TempStoryAir04Category(Base):
    __tablename__ = 'temp_story_air04_category'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    icon = Column(String(255))
    total = Column(Integer)


class TempStoryAir04Subcategory(Base):
    __tablename__ = 'temp_story_air04_subcategory'

    id = Column(BigInteger, primary_key=True)
    categoryid = Column(BigInteger)
    name = Column(String(255))
    value = Column(Integer)
    delta = Column(String(255))
    color = Column(String(255))
    percent = Column(Float)


t_temp_story_air05_airport = Table(
    'temp_story_air05_airport', metadata,
    Column('category', String(255)),
    Column('value', Integer),
    Column('prop', String(255))
)


class TempStoryAir05Color(Base):
    __tablename__ = 'temp_story_air05_colors'

    id = Column(BigInteger, primary_key=True)
    section = Column(String(255), nullable=False)
    color_order = Column(Integer)
    color = Column(String(16))


t_temp_story_air05_country = Table(
    'temp_story_air05_country', metadata,
    Column('category', String(255)),
    Column('value', Integer),
    Column('prop', String(255)),
    Column('nextProp', String(255))
)


class TempStoryAir05Datum(Base):
    __tablename__ = 'temp_story_air05_data'

    id = Column(BigInteger, primary_key=True)
    category = Column(String(255))
    value = Column(Integer)
    prop = Column(String(255))
    nextProp = Column(String(255))


class TempStoryAir05Static(Base):
    __tablename__ = 'temp_story_air05_static'

    id = Column(BigInteger, primary_key=True)
    section_label = Column(String(64), nullable=False)
    section_json = Column(JSON, nullable=False)


class TempStoryHotel01Bar(Base):
    __tablename__ = 'temp_story_hotel01_bar'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    type = Column(String(255))


class TempStoryHotel01BarDatum(Base):
    __tablename__ = 'temp_story_hotel01_bar_data'

    id = Column(BigInteger, primary_key=True)
    barid = Column(BigInteger)
    category = Column(String(255))
    value = Column(Integer)
    delta = Column(Integer)
    change = Column(String(255))
    percent = Column(Float)


class TempStoryHotel01Kpi(Base):
    __tablename__ = 'temp_story_hotel01_kpi'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    value = Column(Integer)
    delta = Column(Integer)
    change = Column(String(255))
    type = Column(String(255))
    icon = Column(String(255))
    percent = Column(Float)


t_temp_story_hotel01_location = Table(
    'temp_story_hotel01_location', metadata,
    Column('title', String(255)),
    Column('radius', Integer),
    Column('latitude', Numeric(10, 7)),
    Column('longitude', Numeric(10, 7))
)


class TempStoryStatic(Base):
    __tablename__ = 'temp_story_static'

    id = Column(BigInteger, primary_key=True)
    section_label = Column(String(64), nullable=False)
    section_json = Column(JSON)


t_v_city = Table(
    'v_city', metadata,
    Column('geo_city_id', BigInteger),
    Column('city_name', String(64)),
    Column('geo_state_id', BigInteger),
    Column('state_name', String(64)),
    Column('state_code', String(8)),
    Column('geo_country_id', BigInteger),
    Column('country_name', String(64)),
    Column('country_code_2char', String(4))
)


class AdvitoApplicationFeature(Base):
    __tablename__ = 'advito_application_feature'

    id = Column(BigInteger, primary_key=True)
    advito_application_id = Column(ForeignKey('advito_application.id'), nullable=False)
    feature_name = Column(String(64), nullable=False)
    feature_tag = Column(String(8), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    description = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application = relationship('AdvitoApplication')


class AdvitoApplicationPersona(Base):
    __tablename__ = 'advito_application_persona'

    id = Column(BigInteger, primary_key=True)
    advito_application_id = Column(ForeignKey('advito_application.id'), nullable=False)
    persona_name = Column(String(32), nullable=False, index=True)
    persona_tag = Column(String(8), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    description = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False)

    advito_application = relationship('AdvitoApplication')


class AdvitoApplicationRole(Base):
    __tablename__ = 'advito_application_role'

    id = Column(BigInteger, primary_key=True)
    advito_application_id = Column(ForeignKey('advito_application.id'), nullable=False)
    role_name = Column(String(64), nullable=False)
    role_tag = Column(String(8), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    description = Column(Text)
    is_assignable = Column(Boolean, nullable=False, server_default=text("true"))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application = relationship('AdvitoApplication')


class BcdGeoCountry(Base):
    __tablename__ = 'bcd_geo_country'

    id = Column(BigInteger, primary_key=True)
    geo_continent_id = Column(ForeignKey('bcd_geo_continent.id'), nullable=False)
    country_name = Column(String(64), nullable=False)
    country_code_2char = Column(String(4), nullable=False, index=True)
    country_code_3char = Column(String(4))
    country_code_numeric = Column(String(4))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    default_currency_code = Column(String(4))
    state_label = Column(String(64))
    master_created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    master_modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    note = Column(Text)
    is_required_in_regions = Column(Boolean, nullable=False, server_default=text("true"))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_continent = relationship('BcdGeoContinent')


class BcdGeoRegion(Base):
    __tablename__ = 'bcd_geo_region'

    id = Column(BigInteger, primary_key=True)
    geo_region_group_id = Column(ForeignKey('bcd_geo_region_group.id'), nullable=False)
    region_name = Column(String(64), nullable=False)
    region_code = Column(String(4))
    region_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_region_group = relationship('BcdGeoRegionGroup')


class Client(Base):
    __tablename__ = 'client'

    id = Column(BigInteger, primary_key=True)
    client_name = Column(String(32), nullable=False)
    client_name_full = Column(String(64), nullable=False)
    client_tag = Column(String(8), nullable=False)
    client_code = Column(String(32))
    lanyon_client_code = Column(String(16))
    gcn = Column(String(16))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    logo_path = Column(String(128))
    description = Column(Text)
    industry = Column(String(64))
    default_currency_code = Column(String(8))
    default_distance_units = Column(String(32))
    geo_region_group_id = Column(ForeignKey('geo_region_group.id'))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    lockreadonly = Column(Boolean)

    geo_region_group = relationship('GeoRegionGroup')


class EmailTemplate(Base):
    __tablename__ = 'email_template'

    id = Column(BigInteger, primary_key=True)
    advito_application_id = Column(ForeignKey('advito_application.id'), nullable=False)
    template_name = Column(String(64), nullable=False)
    template_type = Column(String(64), nullable=False)
    template_note = Column(Text)
    email_subject = Column(String(128), nullable=False)
    email_body = Column(Text, nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application = relationship('AdvitoApplication')


class GeoRegionCountryLink(Base):
    __tablename__ = 'geo_region_country_link'

    Id = Column(BigInteger, primary_key=True)
    geo_region_id = Column(ForeignKey('geo_region.id'), nullable=False)
    geo_country_id = Column(ForeignKey('geo_country.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_country = relationship('GeoCountry')
    geo_region = relationship('GeoRegion')


class GeoState(Base):
    __tablename__ = 'geo_state'

    id = Column(BigInteger, primary_key=True)
    geo_country_id = Column(ForeignKey('geo_country.id'), nullable=False)
    state_name = Column(String(64), nullable=False)
    state_code = Column(String(8))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    master_created = Column(TIMESTAMP(precision=6))
    master_modified = Column(TIMESTAMP(precision=6))
    note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_country = relationship('GeoCountry')


class AdvitoApplicationRoleGroupLink(Base):
    __tablename__ = 'advito_application_role_group_link'

    id = Column(BigInteger, primary_key=True)
    advito_application_role_id = Column(ForeignKey('advito_application_role.id'), nullable=False)
    advito_group_id = Column(ForeignKey('advito_group.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modifed = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application_role = relationship('AdvitoApplicationRole')
    advito_group = relationship('AdvitoGroup')


class AdvitoUser(Base):
    __tablename__ = 'advito_user'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    pwd = Column(String(128), nullable=False, index=True)
    name_last = Column(String(64), nullable=False, index=True)
    name_first = Column(String(64), nullable=False)
    is_enabled = Column(Boolean, nullable=False, server_default=text("false"))
    is_verified = Column(Boolean, nullable=False, server_default=text("false"))
    must_change_pwd = Column(Boolean, nullable=False, server_default=text("false"))
    pwd_expiration = Column(Date)
    email = Column(String(128), nullable=False)
    phone = Column(String(64))
    profile_picture_path = Column(String(256))
    default_timezone = Column(String(128))
    default_language = Column(String(16))
    user_salt = Column(String(64))
    default_date_format = Column(String(32))
    address = Column(String(255))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    client = relationship('Client')


class BcdGeoRegionCountryLink(Base):
    __tablename__ = 'bcd_geo_region_country_link'

    Id = Column(BigInteger, primary_key=True)
    geo_region_id = Column(ForeignKey('bcd_geo_region.id'), nullable=False)
    geo_country_id = Column(ForeignKey('bcd_geo_country.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_country = relationship('BcdGeoCountry')
    geo_region = relationship('BcdGeoRegion')


class BcdGeoState(Base):
    __tablename__ = 'bcd_geo_state'

    id = Column(BigInteger, primary_key=True)
    geo_country_id = Column(ForeignKey('bcd_geo_country.id'), nullable=False)
    state_name = Column(String(64), nullable=False)
    state_code = Column(String(8))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    master_created = Column(TIMESTAMP(precision=6))
    master_modified = Column(TIMESTAMP(precision=6))
    note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_country = relationship('BcdGeoCountry')


class ClientAdvitoApplicationLink(Base):
    __tablename__ = 'client_advito_application_link'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    advito_application_id = Column(ForeignKey('advito_application.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application = relationship('AdvitoApplication')
    client = relationship('Client')


class ClientDivision(Base):
    __tablename__ = 'client_division'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    division_name = Column(String(32), nullable=False)
    division_name_full = Column(String(64), nullable=False)
    division_tag = Column(String(8), nullable=False)
    gcn = Column(String(16))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    description = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    client = relationship('Client')


class ClientFeatureLink(Base):
    __tablename__ = 'client_feature_link'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    advito_application_feature_id = Column(ForeignKey('advito_application_feature.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application_feature = relationship('AdvitoApplicationFeature')
    client = relationship('Client')


class ClientLocation(Base):
    __tablename__ = 'client_location'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))
    location_name = Column(String(64), nullable=False)
    location_tag = Column(String(128))
    location_note = Column(Text)
    address1 = Column(String(64), nullable=False)
    address2 = Column(String(64))
    city = Column(String(64), nullable=False)
    state = Column(String(64))
    postal_code = Column(String(16), nullable=False)
    country = Column(String(64), nullable=False)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    geo_city_id = Column(BigInteger)
    geo_state_id = Column(BigInteger)
    geo_country_id = Column(BigInteger)
    phone = Column(String(32))
    fax = Column(String(32))
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    modified = Column(DateTime, nullable=False, server_default=text("now()"))

    client = relationship('Client')


class ClientMetroArea(Base):
    __tablename__ = 'client_metro_area'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    geo_country_id = Column(BigInteger)
    metro_name = Column(String(128), nullable=False)
    metro_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    client = relationship('Client')


class GeoCity(Base):
    __tablename__ = 'geo_city'

    id = Column(BigInteger, primary_key=True)
    geo_state_id = Column(ForeignKey('geo_state.id'))
    geo_country_id = Column(ForeignKey('geo_country.id'), nullable=False)
    city_name = Column(String(64), nullable=False)
    city_code = Column(String(8))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    master_created = Column(TIMESTAMP(precision=6))
    master_modified = Column(TIMESTAMP(precision=6))
    master_id = Column(BigInteger)
    note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_country = relationship('GeoCountry')
    geo_state = relationship('GeoState')


class GeoSubregion(Base):
    __tablename__ = 'geo_subregion'

    id = Column(BigInteger, primary_key=True)
    geo_region_id = Column(ForeignKey('bcd_geo_region.id'), nullable=False)
    subregion_name = Column(String(64), nullable=False)
    subregion_code = Column(String(4))
    subregion_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_region = relationship('BcdGeoRegion')


class AccessToken(Base):
    __tablename__ = 'access_token'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    token_type = Column(String(32), nullable=False)
    token = Column(String(128), nullable=False, index=True)
    token_expiration = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_user = relationship('AdvitoUser')


class AdvitoUserAccessPrivilege(Base):
    __tablename__ = 'advito_user_access_privilege'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    geo_region_id = Column(ForeignKey('geo_region.id'))
    geo_country_id = Column(ForeignKey('geo_country.id'))
    geo_state_id = Column(ForeignKey('geo_state.id'))
    geo_city_id = Column(ForeignKey('geo_city.id'))
    client_metro_area_id = Column(ForeignKey('client_metro_area.id'))
    access_label = Column(String(64), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_user = relationship('AdvitoUser')
    client_metro_area = relationship('ClientMetroArea')
    geo_city = relationship('GeoCity')
    geo_country = relationship('GeoCountry')
    geo_region = relationship('GeoRegion')
    geo_state = relationship('GeoState')


class AdvitoUserClientdivisionLink(Base):
    __tablename__ = 'advito_user_clientdivision_link'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    client_division_id = Column(ForeignKey('client_division.id'))
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_user = relationship('AdvitoUser')
    client_division = relationship('ClientDivision')


class AdvitoUserClientunitLink(Base):
    __tablename__ = 'advito_user_clientunit_link'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    client_unit_id = Column(ForeignKey('client_division.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_user = relationship('AdvitoUser')
    client_unit = relationship('ClientDivision')


class AdvitoUserGroupLink(Base):
    __tablename__ = 'advito_user_group_link'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    advito_group_id = Column(ForeignKey('advito_group.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_group = relationship('AdvitoGroup')
    advito_user = relationship('AdvitoUser')


class AdvitoUserPersonaLink(Base):
    __tablename__ = 'advito_user_persona_link'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    advito_application_persona_id = Column(ForeignKey('advito_application_persona.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application_persona = relationship('AdvitoApplicationPersona')
    advito_user = relationship('AdvitoUser')


class AdvitoUserRoleLink(Base):
    __tablename__ = 'advito_user_role_link'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    advito_role_id = Column(ForeignKey('advito_application_role.id'), nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_role = relationship('AdvitoApplicationRole')
    advito_user = relationship('AdvitoUser')


class AdvitoUserSession(Base):
    __tablename__ = 'advito_user_session'

    id = Column(BigInteger, primary_key=True)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    session_token = Column(String(128), nullable=False, unique=True)
    session_start = Column(TIMESTAMP(precision=6), nullable=False)
    session_end = Column(TIMESTAMP(precision=6))
    session_duration_sec = Column(Integer)
    session_type = Column(String(32))
    session_expiration = Column(TIMESTAMP(precision=6), nullable=False)
    session_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_user = relationship('AdvitoUser')


class BcdGeoCity(Base):
    __tablename__ = 'bcd_geo_city'

    id = Column(BigInteger, primary_key=True)
    geo_state_id = Column(ForeignKey('bcd_geo_state.id'))
    geo_country_id = Column(ForeignKey('bcd_geo_country.id'), nullable=False)
    city_name = Column(String(64), nullable=False)
    city_code = Column(String(8))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    master_created = Column(TIMESTAMP(precision=6))
    master_modified = Column(TIMESTAMP(precision=6))
    master_id = Column(BigInteger, nullable=False, unique=True)
    note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    geo_country = relationship('BcdGeoCountry')
    geo_state = relationship('BcdGeoState')


class ClientMetroAreaStateLink(Base):
    __tablename__ = 'client_metro_area_state_link'

    id = Column(BigInteger, primary_key=True)
    client_metro_area_id = Column(ForeignKey('client_metro_area.id'), nullable=False)
    geo_state_id = Column(BigInteger, nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    client_metro_area = relationship('ClientMetroArea')


class FileUpload(Base):
    __tablename__ = 'file_upload'

    id = Column(BigInteger, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    upload_datetime = Column(DateTime, nullable=False)
    upload_type = Column(String(32), nullable=False)
    upload_status = Column(String(32))
    upload_details = Column(Text)
    upload_result = Column(String(32))
    filename_original = Column(String(128), nullable=False)
    filename_unique = Column(String(128))
    filename_label = Column(String(64))
    created = Column(DateTime, nullable=False, server_default=text("now()"))
    modified = Column(DateTime, nullable=False, server_default=text("now()"))

    advito_user = relationship('AdvitoUser')
    client = relationship('Client')


class Job(Base):
    __tablename__ = 'job'

    id = Column(BigInteger, primary_key=True)
    advito_application_id = Column(ForeignKey('advito_application.id'), nullable=False)
    advito_user_id = Column(ForeignKey('advito_user.id'), nullable=False)
    client_id = Column(ForeignKey('client.id'))
    program_id = Column(BigInteger)
    job_type = Column(String(32), nullable=False)
    job_detail = Column(Text, nullable=False)
    job_start = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    job_status = Column(String(32))
    job_end = Column(TIMESTAMP(precision=6))
    job_duration_sec = Column(Integer)
    job_result = Column(String(32))
    job_note = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application = relationship('AdvitoApplication')
    advito_user = relationship('AdvitoUser')
    client = relationship('Client')


class AdvitoUserSessionLog(Base):
    __tablename__ = 'advito_user_session_log'

    id = Column(BigInteger, primary_key=True)
    advito_application_id = Column(ForeignKey('advito_application.id'), nullable=False)
    session_token = Column(ForeignKey('advito_user_session.session_token'), nullable=False)
    log_timestamp = Column(DateTime, nullable=False)
    log_action = Column(String(64), nullable=False)
    log_detail = Column(String(64))
    result_code = Column(String(16))
    log_object = Column(String(64))
    log_object_id = Column(BigInteger)
    summary_json = Column(Text)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    advito_application = relationship('AdvitoApplication')
    advito_user_session = relationship('AdvitoUserSession')


class ClientMetroAreaCityLink(Base):
    __tablename__ = 'client_metro_area_city_link'

    id = Column(BigInteger, primary_key=True)
    client_metro_area_id = Column(ForeignKey('client_metro_area.id'), nullable=False)
    geo_city_id = Column(BigInteger, nullable=False)
    created = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))
    modified = Column(TIMESTAMP(precision=6), nullable=False, server_default=text("now()"))

    client_metro_area = relationship('ClientMetroArea')
