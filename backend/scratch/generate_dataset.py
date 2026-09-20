import json
import os

# Create data directory if it doesn't exist
os.makedirs("d:/moneyfollows/backend/data", exist_ok=True)

schemes = []
counter = 1

def S(slug, name, ministry, category, desc, benefits_text, elig_text, docs, app_steps, official_url, tg=None, area=None, age_min=None, age_max=None, gender=None, conf=None, note=None, inc_max=None, inc_note=None):
    global counter
    
    # We will simulate the JSON format requested by the user
    # "category" is passed as a string constant in the original snippet but we'll map it
    cat_map = {
        "AGR": "Agriculture",
        "SOC": "Social Welfare",
        "SKL": "Skills & Employment",
        "UTL": "Utilities"
    }
    
    gender_list = []
    if gender:
        gender_list.append(gender)
        
    residence_list = []
    if area:
        residence_list.append(area)
        
    record = {
        "id": f"scheme_{str(counter).zfill(6)}",
        "name": name,
        "short_name": slug,
        "level": "Central Government",
        "state": None,
        "ministry": ministry,
        "department": None,
        "category": [cat_map.get(category, category)],
        "tags": tg if tg else [],
        "description": desc,
        "benefits": [benefits_text],
        "eligibility": {
            "age": {
                "min": age_min,
                "max": age_max
            },
            "gender": gender_list,
            "social_category": [],
            "annual_income": {
                "min": None,
                "max": inc_max,
                "currency": "INR",
                "note": inc_note
            },
            "occupation": tg if tg else [],
            "education": [],
            "employment_status": [],
            "disability": {
                "required": None,
                "minimum_percentage": None
            },
            "student": None,
            "farmer": "Farmer" in tg if tg else None,
            "residence": residence_list,
            "other_conditions": [elig_text]

        },
        "exclusions": [],
        "documents": docs,
        "application": {
            "mode": [],
            "steps": [app_steps],
            "application_url": official_url if official_url.startswith("http") else None,
            "deadline": None
        },
        "source": {
            "name": "myScheme",
            "url": f"https://www.myscheme.gov.in/schemes/{slug}",
            "official_url": official_url if official_url.startswith("http") else None,
            "official": True
        },
        "status": "prototype_snapshot"
    }
    schemes.append(record)
    counter += 1

MOA = "Ministry of Agriculture & Farmers Welfare"
AGW = "https://agriwelfare.gov.in/"
AGR = "AGR"
SOC = "SOC"
SKL = "SKL"
UTL = "UTL"
EDU = "EDU"
HEA = "HEA"
BUS = "BUS"
LAW = "LAW"
BFI = "BFI"
SPC = "SPC"
HOU = "HOU"
SIT = "SIT"
TRN = "TRN"
V16 = "V16"

NSP = "https://scholarships.gov.in/"
NSP_HOW = "Apply online on the National Scholarship Portal (NSP)."
NSP_DOCS = ["Aadhaar", "Income certificate", "Bank account", "Previous exam marksheet", "Fee receipt"]

S("pm-kisan", "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)", MOA, AGR,
  "Direct income support for landholding farmer families to help with farm inputs and household needs.",
  "₹6,000 per year in three instalments of ₹2,000, paid by DBT into the Aadhaar-seeded bank account.",
  "Landholding farmer families as per land records. Excluded: income-tax payers, institutional landholders, holders of constitutional posts, serving/retired government employees and pensioners drawing ₹10,000+/month (Group D/MTS exempt), and practising professionals (doctors, engineers, lawyers, CAs, architects).",
  ["Aadhaar", "Land ownership records", "Bank account linked to Aadhaar", "Mobile number"],
  "Self-register on the PM-KISAN portal (Farmers Corner) or via a CSC/State nodal officer; complete e-KYC and land-record verification.",
  "https://pmkisan.gov.in/", tg=["Farmer"], area="Rural")

S("pmfby", "Pradhan Mantri Fasal Bima Yojana (PMFBY)", MOA, AGR,
  "Crop insurance against yield loss from natural calamities, pests and diseases for notified crops and areas.",
  "Insurance cover for crop loss. Farmer premium is capped at 2% (kharif food grains/oilseeds), 1.5% (rabi) and 5% (commercial/horticultural crops); the rest is subsidised.",
  "Farmers (owners, tenants, sharecroppers) growing notified crops in notified areas. Enrolment is voluntary.",
  ["Aadhaar", "Bank account", "Land record or tenancy/sharecropping proof", "Sowing declaration"],
  "Enrol before the season cut-off through your bank, a CSC, an insurance-company agent or the National Crop Insurance Portal.",
  "https://pmfby.gov.in/", tg=["Farmer"], area="Rural")

S("kcc", "Kisan Credit Card (KCC)", "Dept. of Financial Services / NABARD / " + MOA, AGR,
  "Revolving credit facility for farmers, tenant farmers, fishers and animal-husbandry farmers to meet crop and allied expenses.",
  "Short-term credit at a subsidised rate under the Modified Interest Subvention Scheme (prompt repayers can get an effective rate around 4%). Limit was raised to ₹5 lakh in 2025.",
  "Individual/joint farmers, tenant farmers, sharecroppers, fishers, animal-husbandry farmers, and SHGs/JLGs of farmers.",
  ["Aadhaar", "PAN (if available)", "Land record or tenancy proof", "Passport photo", "Bank application form"],
  "Apply at any bank branch (commercial, RRB, cooperative) or use the KCC form on the PM-KISAN portal.",
  "https://pmkisan.gov.in/", tg=["Farmer", "Fisher", "Dairy farmer"], area="Rural", conf="medium",
  note="Interest-subvention rates and limits are revised from time to time; confirm with your bank.")

S("enam", "National Agriculture Market (e-NAM)", MOA, AGR,
  "Pan-India electronic trading platform linking APMC mandis so farmers can sell to buyers across markets.",
  "Transparent online price discovery, competitive bidding and direct payment to the seller's bank account.",
  "Farmers, FPOs, traders and commission agents registered with an e-NAM-integrated mandi.",
  ["Aadhaar", "Bank account details / cancelled cheque", "Mobile number", "Crop/land details"],
  "Register on the e-NAM portal or app and complete KYC at the nearest integrated mandi.",
  "https://enam.gov.in/", tg=["Farmer", "Trader"], area="Rural")

S("soil-health-card", "Soil Health Card Scheme", MOA, AGR,
  "Free soil testing with crop-wise nutrient and fertiliser recommendations for each farm.",
  "Free Soil Health Card with recommended fertiliser doses and soil-amendment advice.",
  "All farmers.",
  ["Farmer details", "Land/khasra details"],
  "Register on the Soil Health Card portal or contact the local agriculture office / Krishi Vigyan Kendra for soil sampling.",
  "https://soilhealth.dac.gov.in/", tg=["Farmer"], area="Rural")

S("pmksy-pdmc", "PM Krishi Sinchayee Yojana – Per Drop More Crop", MOA, AGR,
  "Subsidy support for micro-irrigation (drip and sprinkler) to save water and raise yields.",
  "Subsidy on drip/sprinkler systems, generally up to 55% of cost for small/marginal farmers and 45% for others (states may top up).",
  "Farmers with an assured water source; small and marginal farmers get the higher subsidy.",
  ["Aadhaar", "Land records", "Bank account", "Water-source proof", "Supplier quotation"],
  "Apply through the state horticulture/agriculture department portal or the district office.",
  "https://pmksy.gov.in/", tg=["Farmer"], area="Rural", conf="medium", note=V16)

S("pm-kusum", "PM-KUSUM (Solar Pumps and Solarisation)", "Ministry of New & Renewable Energy", AGR,
  "Solar pumps and grid-connected solar power for farmers to cut diesel/electricity cost and earn extra income.",
  "Central and state subsidy (about 30% each for standalone solar pumps; farmer pays the balance), plus option to sell surplus power.",
  "Individual farmers, groups of farmers, cooperatives, panchayats, FPOs and water-user associations.",
  ["Aadhaar", "Land records", "Bank account", "Electricity connection details (for grid-connected pumps)"],
  "Apply through the state nodal agency / DISCOM portal linked from the PM-KUSUM site.",
  "https://pmkusum.mnre.gov.in/", tg=["Farmer"], area="Rural", conf="medium",
  note="Scheme timeline was 31 Mar 2026 in the earlier approval; confirm current status with the state nodal agency.")

S("pkvy", "Paramparagat Krishi Vikas Yojana (PKVY)", MOA, AGR,
  "Cluster-based promotion of organic farming with PGS certification.",
  "Financial assistance per hectare over three years for organic inputs, certification and marketing.",
  "Farmers forming clusters of about 20 hectares (min. 20 farmers) willing to adopt organic farming.",
  ["Aadhaar", "Land records", "Bank account", "Cluster/group membership details"],
  "Apply through the state agriculture department or PGS-India regional council.",
  "https://pgsindia-ncof.gov.in/", tg=["Farmer"], area="Rural", conf="medium", note=V16)

S("nmnf", "National Mission on Natural Farming (NMNF)", MOA, AGR,
  "Mission to promote chemical-free natural farming through farmer training, bio-input resource centres and cluster support.",
  "Training, on-farm demonstrations, bio-input support and certification help for farmers adopting natural farming.",
  "Farmers willing to adopt natural farming, organised in clusters through Gram Panchayats/FPOs.",
  ["Aadhaar", "Land records", "Bank account"],
  "Contact the state agriculture department / KVK to enrol in a natural-farming cluster.",
  AGW, tg=["Farmer"], area="Rural", conf="medium")

S("aif", "Agriculture Infrastructure Fund (AIF)", MOA, AGR,
  "Medium/long-term loan facility for post-harvest and community farming infrastructure such as cold storage, warehouses and processing units.",
  "Interest subvention of 3% per year on loans up to ₹2 crore for up to 7 years, plus CGTMSE credit guarantee cover.",
  "Farmers, FPOs, PACS, cooperatives, SHGs, agri-entrepreneurs and start-ups.",
  ["Aadhaar", "PAN", "Detailed project report", "Land/lease documents", "Bank account"],
  "Apply on the AIF portal; the loan is sanctioned by a participating bank/NBFC.",
  "https://agriinfra.dac.gov.in/", tg=["Farmer", "FPO", "Entrepreneur"], area="Rural")

S("fpo-scheme", "Formation & Promotion of 10,000 Farmer Producer Organisations (FPOs)", MOA, AGR,
  "Central scheme to form and support FPOs so small farmers gain scale in inputs, credit and marketing.",
  "Equity grant, management-cost support for up to 3 years and credit-guarantee cover through implementing agencies (SFAC, NABARD, NCDC).",
  "Groups of farmers (typically 300 in plains, 100 in hilly/NE areas) forming an FPO.",
  ["Aadhaar of members", "Land records", "Bank account", "FPO registration papers"],
  "Approach the implementing agency (SFAC/NABARD/NCDC) through the district agriculture office.",
  "https://www.sfacindia.com/", tg=["Farmer", "FPO"], area="Rural", conf="medium")

S("smam", "Sub-Mission on Agricultural Mechanization (SMAM)", MOA, AGR,
  "Subsidy for buying farm machinery and setting up custom-hiring centres.",
  "Typically 40–50% subsidy on machinery (higher for SC/ST, women and small/marginal farmers); up to 80% for custom-hiring centres in some categories.",
  "Individual farmers, FPOs, cooperatives, SHGs and entrepreneurs.",
  ["Aadhaar", "Land records", "Bank account", "Caste certificate (if claiming higher subsidy)", "Machinery quotation"],
  "Apply on the state agri-mechanization portal (DBT) linked from the SMAM site.",
  "https://agrimachinery.nic.in/", tg=["Farmer"], area="Rural", conf="medium")

S("midh", "Mission for Integrated Development of Horticulture (MIDH)", MOA, AGR,
  "Support for horticulture: planting material, protected cultivation, cold chains and post-harvest units.",
  "Credit-linked back-ended subsidy (commonly up to 35–50% of project cost, depending on component).",
  "Farmers, growers' groups, FPOs and entrepreneurs in horticulture.",
  ["Aadhaar", "Land records", "Bank account", "Project report (for larger components)"],
  "Apply through the State Horticulture Mission / district horticulture office.",
  "https://midh.gov.in/", tg=["Farmer", "Entrepreneur"], area="Rural", conf="medium", note=V16)

S("pm-kmy", "Pradhan Mantri Kisan Maan-Dhan Yojana (PM-KMY)", MOA, SOC,
  "Voluntary contributory pension scheme for small and marginal farmers.",
  "Assured monthly pension of ₹3,000 after age 60; monthly contribution ₹55–₹200 depending on entry age, matched by the Government.",
  "Small and marginal farmers aged 18–40 with cultivable land up to 2 hectares; not covered by NPS/EPFO/ESIC and not income-tax payers.",
  ["Aadhaar", "Land records", "Bank account / savings account", "Mobile number"],
  "Enrol at the nearest CSC or through the Maandhan portal.",
  "https://maandhan.in/", tg=["Farmer", "Senior citizen (future)"], age_min=18, age_max=40, area="Rural")

S("pmmsy", "Pradhan Mantri Matsya Sampada Yojana (PMMSY)", "Ministry of Fisheries, Animal Husbandry & Dairying", AGR,
  "Development of the fisheries sector: fish farming, cold chain, boats, nets and fisher welfare.",
  "Subsidy on eligible projects (commonly 40% for general and 60% for SC/ST/women beneficiaries), plus insurance and livelihood support for fishers.",
  "Fishers, fish farmers, fish workers, SHGs, cooperatives, FFPOs and entrepreneurs.",
  ["Aadhaar", "Bank account", "Fisher ID / cooperative membership (where applicable)", "Project proposal"],
  "Apply through the State Fisheries Department or the PMMSY portal.",
  "https://pmmsy.dof.gov.in/", tg=["Fisher", "Entrepreneur"], conf="medium", note=V16)

S("ahidf", "Animal Husbandry Infrastructure Development Fund (AHIDF)", "Ministry of Fisheries, Animal Husbandry & Dairying", AGR,
  "Loan-linked support to set up dairy, meat-processing and animal-feed plants.",
  "3% interest subvention on loans; credit guarantee cover.",
  "Individuals, MSMEs, FPOs, private companies and Section 8 companies investing in animal-husbandry infrastructure.",
  ["Aadhaar", "PAN", "Detailed project report", "Bank account"],
  "Apply on the AHIDF portal; loans are sanctioned by scheduled banks.",
  "https://ahidf.udyamimitra.in/", tg=["Entrepreneur", "Dairy farmer"], area="Rural", conf="medium", note=V16)

S("nlm", "National Livestock Mission (NLM)", "Ministry of Fisheries, Animal Husbandry & Dairying", AGR,
  "Entrepreneurship support in poultry, sheep, goat, piggery and feed/fodder.",
  "Capital subsidy of up to 50% of project cost (subject to a ceiling) for eligible units.",
  "Individuals, FPOs, SHGs, JLGs, cooperatives and Section 8 companies.",
  ["Aadhaar", "PAN", "Project report", "Bank account", "Land/lease proof"],
  "Apply on the NLM entrepreneurship portal; subsidy is released through the bank loan.",
  "https://nlm.udyamimitra.in/", tg=["Entrepreneur", "Dairy farmer"], area="Rural", conf="medium", note=V16)

S("rgm", "Rashtriya Gokul Mission (RGM)", "Ministry of Fisheries, Animal Husbandry & Dairying", AGR,
  "Development and conservation of indigenous cattle breeds and improvement of milk productivity.",
  "Support for breeding services, artificial insemination, gaushalas and farmer training.",
  "Dairy farmers, breeders, FPOs, SHGs and gaushalas.",
  ["Aadhaar", "Bank account", "Livestock details"],
  "Contact the State Livestock Development Board / district animal-husbandry office.",
  "https://dahd.nic.in/", tg=["Dairy farmer"], area="Rural", conf="medium", note=V16)

S("nbhm", "National Beekeeping & Honey Mission (NBHM)", MOA, AGR,
  "Promotion of scientific beekeeping for higher farm income and pollination.",
  "Training, bee-colony/equipment support and marketing help for beekeepers.",
  "Beekeepers, farmers, FPOs, SHGs and honey-processing entrepreneurs.",
  ["Aadhaar", "Bank account", "Training/registration details"],
  "Apply via the National Bee Board / state horticulture department.",
  "https://nbb.gov.in/", tg=["Farmer", "Entrepreneur"], area="Rural", conf="medium")

S("namo-drone-didi", "Namo Drone Didi", MOA, AGR,
  "Provides drones to women SHGs so they can offer agricultural spraying services on rent.",
  "Central financial assistance of about 80% of drone cost (subject to a cap) plus training for a woman pilot and a helper.",
  "Women self-help groups (SHGs) selected through DAY-NRLM / cluster-level federations.",
  ["SHG registration details", "Aadhaar of members", "Bank account of SHG"],
  "Apply via your SHG federation / district NRLM office or the lead fertiliser company as notified.",
  AGW, tg=["Women SHG"], gender="Female", area="Rural", conf="medium", note=V16)

S("pm-dhan-dhaanya", "PM Dhan-Dhaanya Krishi Yojana", MOA, AGR,
  "Programme to raise farm productivity in about 100 low-productivity agricultural districts by converging existing schemes.",
  "District-level support in irrigation, storage, credit and productivity improvements.",
  "Farmers residing in the selected districts.",
  ["Aadhaar", "Land records", "Bank account"],
  "Access through your district agriculture office; benefits flow via existing schemes.",
  AGW, tg=["Farmer"], area="Rural", conf="medium",
  note="District-based programme; there may be no direct individual application.")

S("pulses-mission", "Mission for Aatmanirbharta in Pulses", MOA, AGR,
  "Mission to raise domestic pulses production with quality seeds, better yields and assured procurement.",
  "Seed support, technical help and assured procurement of tur, urad and masoor at MSP from registered farmers.",
  "Farmers growing pulses who register with the procurement agencies (NAFED/NCCF).",
  ["Aadhaar", "Land records", "Bank account"],
  "Register on the procurement portal notified by NAFED/NCCF through your state agriculture office.",
  AGW, tg=["Farmer"], area="Rural", conf="medium")

S("day-nrlm", "DAY-NRLM (Aajeevika) – National Rural Livelihoods Mission", "Ministry of Rural Development", AGR,
  "Organises rural poor women into SHGs and federations and links them to credit, skills and markets.",
  "SHG revolving fund and community investment support, bank credit with interest subvention, training and enterprise support.",
  "Rural women from poor and vulnerable households (BPL/SECC-identified), forming or joining SHGs.",
  ["Aadhaar", "Bank account", "Ration card / BPL proof"],
  "Contact your Gram Panchayat, Block Mission Manager or nearest SHG/federation to join an SHG.",
  "https://aajeevika.gov.in/", tg=["Woman", "SHG member"], gender="Female", area="Rural")

S("lakhpati-didi", "Lakhpati Didi Initiative", "Ministry of Rural Development", AGR,
  "Initiative to help SHG women build livelihoods that earn at least ₹1 lakh per household per year.",
  "Training, livelihood diversification, credit and market linkages through DAY-NRLM.",
  "Women members of SHGs under DAY-NRLM.",
  ["SHG membership details", "Aadhaar", "Bank account"],
  "Speak to your SHG/village organisation or Block Mission Manager.",
  "https://aajeevika.gov.in/", tg=["Woman", "SHG member"], gender="Female", area="Rural", conf="medium")

S("vb-g-ram-g", "Viksit Bharat – Guarantee for Rozgar and Ajeevika Mission (Gramin) – VB-G RAM G (replaced MGNREGA on 1 Jul 2026)",
  "Ministry of Rural Development", SKL,
  "Statutory rural wage-employment law that replaced MGNREGA from 1 July 2026, with a higher guaranteed number of days.",
  "125 days of guaranteed wage employment per rural household per year; wages by DBT; unemployment allowance if work is not provided on time.",
  "Rural households whose adult members volunteer for unskilled manual work. Existing e-KYC-verified MGNREGA job cards stay valid until new Gramin Rozgar Guarantee Cards are issued.",
  ["Aadhaar", "Job card / Gramin Rozgar Guarantee Card", "Bank or post-office account", "Photograph"],
  "Register at the Gram Panchayat (workers without a job card can still register) and apply for work in writing or via the app.",
  "https://rural.gov.in/", tg=["Rural worker"], area="Rural", age_min=18,
  note="New law in force from 1 Jul 2026; state notifications and wage rates are still being rolled out.")

S("jjm", "Jal Jeevan Mission (Har Ghar Jal)", "Ministry of Jal Shakti", UTL,
  "Provides functional household tap water connections in rural areas.",
  "Tap water connection to every rural household with service delivery via the village water committee.",
  "All rural households without a tap connection.",
  ["Aadhaar", "Household details"],
  "Request a household tap connection through the Gram Panchayat / Village Water & Sanitation Committee.",
  "https://jaljeevanmission.gov.in/", tg=["Household"], area="Rural", conf="medium",
  note="Mission was extended (2028) in the 2025 Budget; confirm ongoing status locally.")

S("sbm-g", "Swachh Bharat Mission (Gramin) Phase II – Individual Household Toilet", "Ministry of Jal Shakti", UTL,
  "Incentive for constructing an individual household latrine in rural areas.",
  "Incentive of ₹12,000 for a toilet for eligible households.",
  "Rural households without a toilet – BPL, SC/ST, small and marginal farmers, landless labourers with homestead, persons with disabilities and women-headed households.",
  ["Aadhaar", "Bank account", "Household / BPL details"],
  "Apply through the Gram Panchayat or the SBM-G portal of your state.",
  "https://swachhbharatmission.ddws.gov.in/", tg=["Household"], area="Rural", conf="medium", note=V16)

WCD = "Ministry of Women & Child Development"
SJE = "Ministry of Social Justice & Empowerment"
MOMA = "Ministry of Minority Affairs"
TRIB = "Ministry of Tribal Affairs"
LAB = "Ministry of Labour & Employment"
MORD = "Ministry of Rural Development"
DFPD = "Dept. of Food & Public Distribution"

# ---------- Women & child ----------
S("pmmvy", "Pradhan Mantri Matru Vandana Yojana (PMMVY)", WCD, SOC,
  "Cash incentive to partly compensate wage loss and support nutrition during pregnancy and lactation.",
  "₹5,000 for the first living child (two instalments) and ₹6,000 in one instalment if the second child is a girl, via DBT.",
  "Pregnant and lactating women aged 19+ for first child (and second child if girl). Not for women employed with the Government/PSUs or already receiving similar statutory maternity benefits.",
  ["Aadhaar", "MCP (Mother-Child Protection) card", "Bank/post-office account", "Identity proof"],
  "Register at the nearest Anganwadi Centre / health facility or on the PMMVY portal.",
  "https://pmmvy.wcd.gov.in/", tg=["Pregnant woman", "Lactating mother"], gender="Female", age_min=19)

S("mission-shakti", "Mission Shakti (Sambal & Samarthya)", WCD, SOC,
  "Umbrella mission for women's safety and empowerment: One Stop Centres, Women Helpline 181, Shakti Sadan/Swadhar, working women hostels, creches and gender-budget support.",
  "Emergency rescue, shelter, counselling, legal and medical aid, creche services and hostel accommodation.",
  "Women in distress, working women and children needing care, as per the component.",
  ["Identity proof (not mandatory for emergency help)"],
  "Call 181 or approach the nearest One Stop Centre / district WCD office.",
  "https://wcd.gov.in/", tg=["Woman", "Girl child"], gender="Female", conf="medium", note=V16)

S("bbbp", "Beti Bachao Beti Padhao (BBBP)", WCD, SOC,
  "Campaign and district-level programme to improve child sex ratio and promote girls' education.",
  "Awareness, school enrolment drives and convergence with education and health services (no direct cash benefit).",
  "Girl child and families, through district administration.",
  ["Not applicable"],
  "Engage with the district WCD office, schools and Anganwadi centres.",
  "https://wcd.gov.in/", tg=["Girl child"], gender="Female", conf="medium",
  note="Awareness scheme; no individual application or cash benefit.")

S("poshan-2", "Saksham Anganwadi & Poshan 2.0", WCD, SOC,
  "Nutrition and early-childhood-care programme through Anganwadi Centres.",
  "Supplementary nutrition, pre-school education, immunisation and health referrals for children 0–6 years, pregnant women and lactating mothers; nutrition support for adolescent girls in designated areas.",
  "Children 0–6 years, pregnant and lactating women, adolescent girls (per scheme norms).",
  ["Aadhaar (for beneficiary registration)", "MCP card (for mothers)"],
  "Register at your nearest Anganwadi Centre.",
  "https://poshanabhiyaan.gov.in/", tg=["Child", "Pregnant woman", "Lactating mother"], age_max=6, conf="medium", note=V16)

S("mission-vatsalya", "Mission Vatsalya (Child Protection)", WCD, SOC,
  "Child-protection mission covering institutional care, foster care, adoption and sponsorship for children in need.",
  "Sponsorship support (about ₹4,000 per child per month) and shelter, education and counselling for eligible children.",
  "Children in need of care and protection, orphans and children in difficult circumstances (up to 18 years).",
  ["Child's identity/birth proof", "Recommendation of Child Welfare Committee / district child protection unit"],
  "Approach the District Child Protection Unit or Child Welfare Committee; Childline 1098 for emergencies.",
  "https://wcd.gov.in/", tg=["Child", "Orphan"], age_max=18, conf="medium", note=V16)

# ---------- Pensions & social assistance (NSAP) ----------
NSAP_URL = "https://nsap.nic.in/"
S("ignoaps", "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)", MORD, SOC,
  "Monthly pension for elderly persons from BPL households under the National Social Assistance Programme.",
  "Central pension of ₹200 per month (age 60–79) and ₹500 per month (age 80+); many states add their own top-up.",
  "Indian citizens aged 60+ belonging to a BPL household.",
  ["Age proof", "BPL certificate/ration card", "Aadhaar", "Bank account"],
  "Apply through the Gram Panchayat / urban local body or the state social-welfare pension portal.",
  NSAP_URL, tg=["Senior citizen", "BPL"], age_min=60, conf="medium",
  note="Central amounts are fixed; state top-ups and application portals vary.")

S("ignwps", "Indira Gandhi National Widow Pension Scheme (IGNWPS)", MORD, SOC,
  "Monthly pension for widows from BPL households.",
  "Central pension of ₹300 per month (age 40–79); states may top up.",
  "Widows aged 40–79 years from BPL households.",
  ["Husband's death certificate", "Age proof", "BPL proof", "Aadhaar", "Bank account"],
  "Apply through the Gram Panchayat / urban local body or the state pension portal.",
  NSAP_URL, tg=["Widow", "BPL"], gender="Female", age_min=40, age_max=79, conf="medium",
  note="Central amount is fixed; state top-ups and portals vary.")

S("igndps", "Indira Gandhi National Disability Pension Scheme (IGNDPS)", MORD, SOC,
  "Monthly pension for persons with severe or multiple disabilities from BPL households.",
  "Central pension of ₹300 per month (age 18–79); states may top up.",
  "Persons aged 18–79 with 80% or more disability, or multiple disabilities, from BPL households.",
  ["Disability certificate / UDID", "BPL proof", "Aadhaar", "Bank account"],
  "Apply through the Gram Panchayat / urban local body or the state pension portal.",
  NSAP_URL, tg=["Person with disability", "BPL"], age_min=18, age_max=79, conf="medium",
  note="Central amount is fixed; state top-ups and portals vary.")

S("nfbs", "National Family Benefit Scheme (NFBS)", MORD, SOC,
  "One-time assistance to a BPL family on the death of its primary breadwinner.",
  "Lump-sum assistance of ₹20,000.",
  "BPL households in which the primary breadwinner (aged 18–59) has died.",
  ["Death certificate", "BPL proof", "Aadhaar", "Bank account", "Family details"],
  "Apply through the Gram Panchayat / urban local body or the state social-welfare portal.",
  NSAP_URL, tg=["BPL", "Bereaved family"], conf="medium")

S("rvy", "Rashtriya Vayoshri Yojana (RVY)", SJE, SOC,
  "Free physical aids and assisted-living devices for BPL senior citizens with age-related disabilities.",
  "Free devices such as walking sticks, hearing aids, wheelchairs, spectacles and dentures, distributed in camps.",
  "Senior citizens aged 60+ belonging to BPL families (or with income up to ₹15,000/month) with age-related disability.",
  ["Age proof", "BPL card / income proof", "Aadhaar", "Passport photo"],
  "Register at ALIMCO/district-level distribution camps announced by the district administration.",
  "https://socialjustice.gov.in/", tg=["Senior citizen", "BPL"], age_min=60, conf="medium", note=V16)

# ---------- Persons with disabilities ----------
S("adip", "ADIP Scheme – Assistive Devices for Persons with Disabilities", "Dept. of Empowerment of Persons with Disabilities", SOC,
  "Free or subsidised aids and appliances to enhance mobility and independence.",
  "Devices provided free if monthly income is up to ₹15,000, and at 50% cost if income is ₹15,001–₹22,500.",
  "Indian citizens with at least 40% disability holding a disability certificate/UDID.",
  ["Disability certificate / UDID", "Income proof", "Aadhaar", "Passport photo"],
  "Apply through ALIMCO or the implementing agency at camps announced by the district administration.",
  "https://disabilityaffairs.gov.in/", tg=["Person with disability"], conf="medium", note=V16)

S("udid", "Unique Disability ID (UDID) / Swavlamban Card", "Dept. of Empowerment of Persons with Disabilities", SOC,
  "Single national ID and certificate for persons with disabilities to access benefits across schemes.",
  "Nationally valid disability certificate and ID card used for pensions, concessions and scholarships.",
  "Persons with one or more of the disabilities recognised under the RPwD Act, 2016.",
  ["Aadhaar", "Medical records", "Passport photo", "Address proof"],
  "Apply online on the UDID portal and attend the medical assessment at the designated hospital.",
  "https://www.swavlambancard.gov.in/", tg=["Person with disability"])

S("pwd-prematric", "Pre-Matric Scholarship for Students with Disabilities", "Dept. of Empowerment of Persons with Disabilities", EDU,
  "Scholarship for school students with disabilities in classes 9–10.",
  "Monthly scholarship, book grant and disability allowance as per norms.",
  "Students with 40%+ disability in classes 9–10; family income up to ₹2.5 lakh per year.",
  NSP_DOCS[:1] + ["Disability certificate / UDID", "Income certificate", "Marksheet", "Bank account"],
  NSP_HOW, NSP, tg=["Student", "Person with disability"], conf="medium", note=V16)

S("pwd-postmatric", "Post-Matric Scholarship for Students with Disabilities", "Dept. of Empowerment of Persons with Disabilities", EDU,
  "Scholarship for students with disabilities pursuing class 11 to postgraduate/professional courses.",
  "Maintenance allowance, reimbursement of compulsory fees and disability allowance as per norms.",
  "Students with 40%+ disability in class 11 and above; family income up to ₹2.5 lakh per year.",
  NSP_DOCS[:1] + ["Disability certificate / UDID", "Income certificate", "Marksheet", "Bank account"],
  NSP_HOW, NSP, tg=["Student", "Person with disability"], conf="medium", note=V16)

S("pwd-topclass", "Top Class Education for Students with Disabilities", "Dept. of Empowerment of Persons with Disabilities", EDU,
  "Full financial support for students with disabilities admitted to notified premier institutions.",
  "Tuition/non-refundable fees, living expenses, books and computer allowance.",
  "Students with 40%+ disability admitted to notified top institutions; family income up to ₹6 lakh per year.",
  NSP_DOCS[:1] + ["Disability certificate / UDID", "Income certificate", "Admission proof", "Bank account"],
  NSP_HOW, NSP, tg=["Student", "Person with disability"], conf="medium", note=V16)

S("niramaya", "Niramaya Health Insurance Scheme (National Trust)", "The National Trust (Ministry of Social Justice & Empowerment)", HEA,
  "Affordable health insurance for persons with autism, cerebral palsy, intellectual disability and multiple disabilities.",
  "Health cover up to ₹1 lakh per year; premium about ₹250 (BPL) or ₹500 (others) per year.",
  "Persons with the four National Trust disabilities, subject to registration.",
  ["Disability certificate", "Aadhaar", "BPL proof (for the lower premium)", "Passport photo"],
  "Apply through a National Trust registered organisation or the Trust's portal.",
  "https://thenationaltrust.gov.in/", tg=["Person with disability"], conf="medium")

S("nhfdc", "NHFDC Concessional Loans for Persons with Disabilities", "National Handicapped Finance & Development Corporation", BUS,
  "Concessional loans for self-employment and skill training for persons with disabilities.",
  "Loans at concessional interest through State Channelising Agencies and banks; extra support for women.",
  "Persons with 40%+ disability aged 18–60 who are Indian citizens.",
  ["Disability certificate / UDID", "Aadhaar", "Project report", "Income and address proof"],
  "Apply through the State Channelising Agency or the NHFDC portal.",
  "https://nhfdc.nic.in/", tg=["Person with disability", "Entrepreneur"], age_min=18, age_max=60, conf="medium")

# ---------- SC / ST / OBC scholarships and support ----------
S("sc-postmatric", "Post-Matric Scholarship for Scheduled Caste Students", SJE, EDU,
  "Financial assistance for SC students studying after class 10 (class 11 to PhD).",
  "Maintenance allowance plus payment/reimbursement of compulsory non-refundable fees as per norms.",
  "SC students in post-matric courses; parental income up to ₹2.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium",
  note="In Mar 2026 the ministry told a parliamentary panel it plans to raise the income ceiling to ₹4.5 lakh and cap course fees; confirm current rules on NSP.")

S("sc-prematric", "Pre-Matric Scholarship for Scheduled Caste Students (Class 9–10)", SJE, EDU,
  "Scholarship for SC students in classes 9 and 10.",
  "Monthly scholarship for day scholars/hostellers plus an annual ad-hoc grant.",
  "SC students studying in classes 9–10; parental income up to ₹2.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("st-prematric", "Pre-Matric Scholarship for Scheduled Tribe Students (Class 9–10)", TRIB, EDU,
  "Scholarship for ST students in classes 9 and 10.",
  "Monthly scholarship for day scholars/hostellers plus an annual ad-hoc grant.",
  "ST students studying in classes 9–10; parental income up to ₹2.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("st-postmatric", "Post-Matric Scholarship for Scheduled Tribe Students", TRIB, EDU,
  "Financial assistance for ST students in post-matric courses.",
  "Maintenance allowance and reimbursement of compulsory fees as per norms.",
  "ST students in class 11 and above; parental income up to ₹2.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("pm-yasasvi", "PM YASASVI Scholarships (OBC, EBC and DNT Students)", SJE, EDU,
  "Umbrella scheme of pre-matric and post-matric scholarships for OBC, EBC and denotified/nomadic tribe students.",
  "Annual scholarship support for classes 9–12 and higher education as per component norms.",
  "OBC/EBC/DNT students meeting the merit criteria; parental income up to ₹2.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("top-class-sc", "Top Class Education Scheme for Scheduled Caste Students", SJE, EDU,
  "Full financial support for SC students admitted to notified top institutions.",
  "Tuition fees, living expenses, books and computer allowance as per norms.",
  "SC students admitted to notified institutions; family income up to ₹8 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("nos-sc", "National Overseas Scholarship (SC, DNT and Landless Agricultural Labourers)", SJE, EDU,
  "Scholarship for postgraduate and PhD study abroad for selected disadvantaged groups.",
  "Tuition, living allowance, airfare and visa costs as per norms for selected candidates.",
  "SC, denotified tribes, semi-nomadic, landless agricultural labourers and traditional artisans; family income up to ₹8 lakh per year; age limit applies.",
  ["Aadhaar", "Caste and income certificate", "Admission letter from foreign university", "Academic records"],
  "Apply on the ministry's National Overseas Scholarship portal when applications open.",
  "https://nosmsje.gov.in/", tg=["Student"], conf="medium", note=V16)

S("pm-daksh", "PM-DAKSH (Skilling for SC, OBC, DNT, Safai Karamcharis and Waste Pickers)", SJE, SKL,
  "Free skill development and upskilling programmes for marginalised target groups.",
  "Free training (up-skilling, re-skilling, short-term and long-term) and placement support.",
  "SC, OBC, EBC, DNT, safai karamcharis and waste pickers aged 18–45.",
  ["Aadhaar", "Caste/category certificate", "Educational documents", "Bank account"],
  "Register on the PM-DAKSH portal and choose an empanelled training centre.",
  "https://pmdaksh.dosje.gov.in/", tg=["Youth", "Job seeker"], age_min=18, age_max=45, conf="medium", note=V16)

S("nsfdc", "NSFDC Concessional Loans for Scheduled Caste Beneficiaries", "National Scheduled Castes Finance & Development Corporation", BUS,
  "Concessional loans for income-generating activities of SC beneficiaries.",
  "Low-interest term loans for micro-enterprise projects through State Channelising Agencies.",
  "SC individuals with family income below the limit set by the scheme.",
  ["Caste certificate", "Income certificate", "Aadhaar", "Project details", "Bank account"],
  "Apply through your State Channelising Agency or the NSFDC portal.",
  "https://nsfdc.nic.in/", tg=["Entrepreneur"], conf="medium",
  note="Income ceilings and loan limits are set in the current scheme guidelines; check with the channelising agency.")

S("nskfdc", "NSKFDC Schemes for Safai Karamcharis and Waste Pickers", "National Safai Karamcharis Finance & Development Corporation", BUS,
  "Concessional loans and skill training for safai karamcharis, manual scavengers and their dependents.",
  "Low-interest loans for self-employment and free skill training with stipend.",
  "Safai karamcharis, identified manual scavengers and their dependents.",
  ["Identity proof", "Caste/occupation proof", "Project details", "Bank account"],
  "Apply through State Channelising Agencies or banks; details on the NSKFDC site.",
  "https://nskfdc.nic.in/", tg=["Entrepreneur", "Sanitation worker"], conf="medium")

S("nbcfdc", "NBCFDC Concessional Loans for OBC Beneficiaries", "National Backward Classes Finance & Development Corporation", BUS,
  "Concessional loans for self-employment and education among backward-class families.",
  "Term loans at low interest for income-generating activities and education.",
  "OBC families below the income limit prescribed by the corporation.",
  ["Caste certificate", "Income certificate", "Aadhaar", "Project details", "Bank account"],
  "Apply through State Channelising Agencies or the NBCFDC portal.",
  "https://nbcfdc.gov.in/", tg=["Entrepreneur"], conf="medium",
  note="Income ceilings and loan limits change; check current guidelines.")

S("nmdfc", "NMDFC Concessional Loans for Minorities", "National Minorities Development & Finance Corporation", BUS,
  "Concessional loans to minority communities for self-employment and education.",
  "Term loans at concessional interest through State Channelising Agencies.",
  "Members of notified minority communities (Muslims, Christians, Sikhs, Buddhists, Jains, Parsis) below the income limit set by the scheme.",
  ["Minority-community proof", "Income certificate", "Aadhaar", "Project details", "Bank account"],
  "Apply through State Channelising Agencies or the NMDFC portal.",
  "https://nmdfc.org/", tg=["Entrepreneur"], conf="medium",
  note="Income ceilings and loan limits change; check current guidelines.")

S("ambedkar-intercaste", "Dr. Ambedkar Scheme for Social Integration through Inter-Caste Marriage", "Dr. Ambedkar Foundation (MoSJE)", SOC,
  "Incentive to couples in a valid inter-caste marriage where one spouse is a Scheduled Caste person.",
  "₹2.5 lakh incentive to the couple (part as a fixed deposit).",
  "Couples where one spouse is SC and the other is non-SC, marriage registered under the Hindu Marriage Act, first marriage for both; combined annual income up to about ₹5 lakh; apply within one year of marriage.",
  ["Marriage certificate", "Caste certificate of the SC spouse", "Aadhaar", "Income certificate", "Bank account"],
  "Apply through the state/district social-welfare office with recommendation of the district magistrate, or the Foundation's portal.",
  "https://www.ambedkarfoundation.nic.in/", tg=["Couple"], conf="medium", note=V16)

S("pre-minority", "Pre-Matric Scholarship for Minorities (Class 9–10)", MOMA, EDU,
  "Scholarship for minority-community students in classes 9–10.",
  "Annual scholarship covering admission/tuition fees, maintenance allowance and books.",
  "Students from notified minorities with at least 50% marks in the previous exam; family income up to ₹1 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("post-minority", "Post-Matric Scholarship for Minorities", MOMA, EDU,
  "Scholarship for minority students in class 11 up to PhD.",
  "Annual scholarship for admission/tuition fees and maintenance allowance.",
  "Students from notified minorities with at least 50% marks in the previous exam; family income up to ₹2 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("mcm-minority", "Merit-cum-Means Scholarship for Minority Students (Professional & Technical Courses)", MOMA, EDU,
  "Scholarship for minority students in professional and technical UG/PG courses.",
  "Course-fee reimbursement and maintenance allowance.",
  "Students from notified minorities with at least 50% marks; family income up to ₹2.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], conf="medium", note=V16)

S("emrs", "Eklavya Model Residential Schools (EMRS)", TRIB, EDU,
  "Free residential CBSE-pattern schools for Scheduled Tribe students from class 6 to 12.",
  "Free education, boarding, lodging, uniforms and books.",
  "Scheduled Tribe students admitted through the entrance test (NESTS).",
  ["ST certificate", "Aadhaar", "Birth proof", "Previous class marksheet"],
  "Apply during the annual EMRS admission window via the EMRS portal or district tribal office.",
  "https://emrs.tribal.gov.in/", tg=["Student"], age_min=10, age_max=18, area="Rural", conf="medium")

S("pm-janman", "PM-JANMAN (PM Janjati Adivasi Nyaya Maha Abhiyan)", TRIB, SOC,
  "Mission to saturate basic services for Particularly Vulnerable Tribal Groups (PVTGs).",
  "Pucca houses, roads, drinking water, electricity, mobile medical units, hostels and skilling for PVTG habitations.",
  "Members of the 75 Particularly Vulnerable Tribal Groups.",
  ["Aadhaar", "ST/PVTG certificate", "Ration card"],
  "Access through the Gram Panchayat/district tribal welfare office; benefits are delivered via convergence with other schemes.",
  "https://tribal.nic.in/", tg=["Tribal family"], area="Rural", conf="medium", note=V16)

S("dajgua", "Dharti Aaba Janjatiya Gram Utkarsh Abhiyan (DAJGUA)", TRIB, SOC,
  "Saturation of basic services in tribal-majority villages and aspirational tribal blocks.",
  "Housing, water, electricity, health, education and livelihood support through convergence.",
  "Scheduled Tribe households in covered villages.",
  ["Aadhaar", "ST certificate", "Ration card"],
  "Access through the Gram Panchayat and district tribal welfare office.",
  "https://tribal.nic.in/", tg=["Tribal family"], area="Rural", conf="medium", note=V16)

S("van-dhan", "Pradhan Mantri Van Dhan Yojana (PM Janjatiya Vikas Mission)", TRIB, BUS,
  "Value addition and marketing of minor forest produce through tribal SHGs and Van Dhan Vikas Kendras.",
  "Training, equipment and market linkage for tribal SHG members.",
  "Tribal gatherers and artisans organised in SHGs.",
  ["Aadhaar", "ST certificate", "SHG details", "Bank account"],
  "Join or form a Van Dhan SHG through TRIFED or the state tribal department.",
  "https://trifed.tribal.gov.in/", tg=["Tribal entrepreneur", "SHG member"], area="Rural", conf="medium", note=V16)

S("smile", "SMILE – Support for Marginalised Individuals for Livelihood and Enterprise", SJE, SOC,
  "Comprehensive rehabilitation for transgender persons and persons engaged in begging.",
  "Skill training, livelihood support, shelter (Garima Greh) and medical facilitation.",
  "Transgender persons and persons engaged in begging.",
  ["Identity proof", "Transgender certificate / ID (for transgender persons)"],
  "Register on the National Portal for Transgender Persons or contact the district social-welfare office.",
  "https://socialjustice.gov.in/", tg=["Transgender person", "Person engaged in begging"], conf="medium", note=V16)

S("namaste", "NAMASTE (National Action for Mechanised Sanitation Ecosystem)", SJE + " & Ministry of Housing & Urban Affairs", SOC,
  "Support for sanitation workers: profiling, safety gear, health insurance and alternative livelihoods.",
  "Occupational-safety equipment, health insurance and capital subsidy/loan support for sanitation workers and waste pickers.",
  "Sewer and septic-tank workers and waste pickers in urban local bodies.",
  ["Identity proof", "Worker profiling details"],
  "Enrol through your urban local body / NAMASTE profiling drive.",
  "https://socialjustice.gov.in/", tg=["Sanitation worker", "Waste picker"], area="Urban", conf="medium", note=V16)

# ---------- Food security ----------
S("aay", "Antyodaya Anna Yojana (AAY)", DFPD, SOC,
  "Highest-priority ration-card category under the National Food Security Act for the poorest households.",
  "35 kg of foodgrains per family per month (free under PMGKAY).",
  "Poorest-of-the-poor households identified by the state – e.g., landless labourers, marginal farmers, widows, terminally ill, disabled and elderly persons without support.",
  ["Aadhaar of members", "Address proof", "Income/BPL proof", "Passport photo"],
  "Apply for a ration card at the state food & civil supplies portal or your nearest Fair Price Shop / block office.",
  "https://nfsa.gov.in/", tg=["Poor household"], conf="medium", note="Identification criteria and application portals differ by state.")

S("phh", "Priority Household (PHH) Ration Card under NFSA", DFPD, SOC,
  "Ration-card category covering priority households under the National Food Security Act.",
  "5 kg of foodgrains per person per month (free under PMGKAY).",
  "Households identified by the state under NFSA criteria (coverage: up to 75% of rural and 50% of urban population).",
  ["Aadhaar of members", "Address proof", "Income proof", "Passport photo"],
  "Apply on the state food & civil supplies portal or at your block/ward office.",
  "https://nfsa.gov.in/", tg=["Household"], conf="medium", note="State-specific eligibility and application portal.")

S("pmgkay", "Pradhan Mantri Garib Kalyan Anna Yojana (PMGKAY)", DFPD, SOC,
  "Free foodgrains to all NFSA ration-card holders.",
  "5 kg of free foodgrains per person per month for AAY/PHH beneficiaries (extended for five years from 1 Jan 2024).",
  "Households holding AAY or PHH ration cards under NFSA.",
  ["Ration card", "Aadhaar"],
  "No separate application: collect grain from your Fair Price Shop using your ration card (Aadhaar-authenticated).",
  "https://dfpd.gov.in/", tg=["Poor household"], conf="medium", note="Confirm the current period on the DFPD website.")

S("onorc", "One Nation One Ration Card (ONORC)", DFPD, SOC,
  "Nationwide portability of ration cards so beneficiaries can draw their entitlement anywhere in India.",
  "Collect your NFSA entitlement from any Fair Price Shop across states via biometric/Aadhaar authentication.",
  "Existing NFSA ration-card holders, especially migrant workers and families.",
  ["Ration card", "Aadhaar (biometric authentication)"],
  "Visit any FPS with e-PoS device; check status on the Mera Ration app / IMPDS portal.",
  "https://impds.nic.in/", tg=["Migrant worker", "Household"])

# ---------- Labour & unorganised workers ----------
S("e-shram", "e-Shram – National Database of Unorganised Workers", LAB, SOC,
  "Registration of unorganised workers to give them a UAN-linked e-Shram card and access to social-security benefits.",
  "e-Shram card/UAN; accidental death/disability insurance cover of ₹2 lakh under PMSBY (first-year premium borne by the Government) and preference for other social-security schemes.",
  "Unorganised workers aged 16–59 who are not members of EPFO/ESIC/NPS and are not income-tax payers.",
  ["Aadhaar", "Mobile number linked to Aadhaar", "Bank account"],
  "Self-register on the e-Shram portal/app or at any CSC.",
  "https://eshram.gov.in/", tg=["Unorganised worker"], age_min=16, age_max=59)

S("pm-sym", "Pradhan Mantri Shram Yogi Maan-Dhan (PM-SYM)", LAB, SOC,
  "Voluntary contributory pension scheme for unorganised workers.",
  "Assured monthly pension of ₹3,000 after age 60; monthly contribution ₹55–₹200 by entry age, matched by the Government.",
  "Unorganised workers aged 18–40 with monthly income up to ₹15,000, not covered by EPFO/ESIC/NPS and not income-tax payers.",
  ["Aadhaar", "Savings bank account / Jan Dhan account", "Mobile number"],
  "Enrol at a CSC or through the Maandhan portal.",
  "https://maandhan.in/", tg=["Unorganised worker"], age_min=18, age_max=40)

S("pm-lvm", "Pradhan Mantri Laghu Vyapari Maan-Dhan (PM-LVM)", "Ministry of Labour & Employment", SOC,
  "Voluntary pension scheme for small shopkeepers, retail traders and self-employed persons.",
  "Assured monthly pension of ₹3,000 after age 60 with matching Government contribution.",
  "Shopkeepers, retail traders and self-employed persons aged 18–40 with annual turnover up to ₹1.5 crore, not covered by EPFO/ESIC/NPS and not income-tax payers.",
  ["Aadhaar", "Savings bank account", "GST/turnover self-declaration"],
  "Enrol at a CSC or through the Maandhan portal.",
  "https://maandhan.in/", tg=["Trader", "Self-employed"], age_min=18, age_max=40, conf="medium")

S("esic", "ESIC Medical and Cash Benefits (Employees' State Insurance)", LAB, HEA,
  "Social-security and health insurance for workers in covered establishments.",
  "Full medical care for the worker and family, sickness and maternity benefit, disablement and dependants' benefit, funeral expenses.",
  "Employees in covered factories/establishments with monthly wages up to ₹21,000 (₹25,000 for persons with disability).",
  ["Aadhaar", "Employer registration details", "Bank account", "Family details"],
  "Registered by the employer; insured persons get an IP number through the ESIC portal.",
  "https://www.esic.gov.in/", tg=["Employee"], conf="medium")

S("epf", "Employees' Provident Fund & Pension Schemes (EPF, EPS, EDLI)", LAB, BFI,
  "Retirement savings, pension and life insurance for salaried employees.",
  "Provident-fund savings with interest, monthly pension after retirement, and insurance cover for dependants.",
  "Employees in covered establishments; membership is mandatory for those earning up to the statutory wage ceiling (₹15,000/month) and optional above it.",
  ["Aadhaar", "Bank account", "PAN (recommended)", "UAN / employer details"],
  "Enrolment is done by the employer; members manage their UAN on the EPFO Member Portal.",
  "https://www.epfindia.gov.in/", tg=["Employee"], conf="medium",
  note="Wage ceiling and rules can change under the labour codes; confirm on the EPFO site.")

S("bocw", "Building & Other Construction Workers (BOCW) Welfare Board Schemes", LAB, SOC,
  "State welfare boards provide benefits such as education aid, medical help, maternity benefit and pension to registered construction workers.",
  "Scholarships for children, medical/maternity assistance, accident compensation and pension (amounts vary by state).",
  "Construction workers aged 18–60 who worked at least 90 days in the last 12 months.",
  ["Aadhaar", "90-day work certificate", "Bank account", "Passport photo"],
  "Register with your state BOCW Welfare Board (online portal or labour office).",
  "https://labour.gov.in/", tg=["Construction worker"], age_min=18, age_max=60, conf="medium", note="Benefits and application portal differ by state.")

S("eli-pmvbry", "Employment Linked Incentive (PM Viksit Bharat Rozgar Yojana)", LAB, SKL,
  "Incentive scheme to encourage formal job creation for first-time employees and employers.",
  "First-time employees get up to one month's EPF wage (max ₹15,000) in two instalments; employers get up to ₹3,000 per month per additional hire for two years (longer for manufacturing).",
  "First-time EPFO-registered employees earning up to ₹1 lakh/month in jobs created between 1 Aug 2025 and 31 Jul 2027, and their employers.",
  ["Aadhaar", "UAN activated with Aadhaar-based face authentication", "Bank account"],
  "Benefits flow automatically via EPFO if the employer and employee meet UAN/Aadhaar-seeding conditions.",
  "https://www.epfindia.gov.in/", tg=["Job seeker", "Employee", "Employer"], conf="medium", note="Confirm operational guidelines on the EPFO/Labour Ministry site.")

# ---------- Legal aid ----------
S("nalsa-legal-aid", "Free Legal Aid (NALSA / State Legal Services Authorities)", "National Legal Services Authority", LAW,
  "Free legal representation, advice and Lok Adalat services for eligible persons.",
  "Free lawyer, court-fee exemption and legal advice.",
  "Women, children, SC/ST, persons with disabilities, victims of trafficking or disasters, industrial workers, persons in custody, and persons below the income limit fixed by the State Legal Services Authority.",
  ["Identity proof", "Income proof (where applicable)", "Case details"],
  "Apply at the District/State Legal Services Authority or the NALSA online portal; helpline 15100.",
  "https://nalsa.gov.in/", tg=["Litigant"], conf="medium", note="Income ceiling is set by each State Legal Services Authority.")

S("tele-law", "Tele-Law (Legal Advice through CSCs)", "Ministry of Law & Justice", LAW,
  "Free pre-litigation legal advice by video/telephone via Common Service Centres.",
  "Free advice from panel lawyers; free for eligible groups (women, SC/ST, disabled, etc.).",
  "Any citizen; free service for groups eligible for legal aid, otherwise nominal fee.",
  ["Aadhaar / identity proof"],
  "Visit a nearby CSC or use the Tele-Law mobile app.",
  "https://www.tele-law.in/", tg=["Citizen"], area="Rural", conf="medium")

MOE = "Ministry of Education"
MOHFW = "Ministry of Health & Family Welfare"
NHA = "National Health Authority"
MSDE = "Ministry of Skill Development & Entrepreneurship"

# ---------- Education ----------
S("pm-poshan", "PM POSHAN (Mid-Day Meal Scheme)", MOE, EDU,
  "Hot cooked meal for children in government and aided schools to improve enrolment, attendance and nutrition.",
  "Free hot meal on school days for pre-primary to class 8 students.",
  "Students of government, government-aided and local-body schools (pre-primary to class 8).",
  ["School enrolment (no application needed)"],
  "Automatic for enrolled students; the school implements the scheme.",
  "https://pmposhan.education.gov.in/", tg=["Student"], age_min=3, age_max=14, conf="medium", note=V16)

S("samagra-shiksha", "Samagra Shiksha Abhiyan", MOE, EDU,
  "Integrated school-education programme from pre-school to class 12.",
  "Free textbooks, uniforms for eligible groups, transport/escort support, KGBV hostels, inclusive-education support for children with special needs.",
  "Students in government schools (with additional support for girls, SC/ST and children with special needs).",
  ["School enrolment (no application needed)"],
  "Access through the school / block education office.",
  "https://samagra.education.gov.in/", tg=["Student"], conf="medium", note=V16)

S("kgbv", "Kasturba Gandhi Balika Vidyalaya (KGBV)", MOE, EDU,
  "Residential upper-primary and secondary schools for girls in educationally backward blocks.",
  "Free residential education, food, books and uniforms.",
  "Girls from SC, ST, OBC, minority communities and BPL families (priority to dropouts and out-of-school girls).",
  ["Aadhaar", "Birth/age proof", "Category/BPL certificate", "Previous school records"],
  "Apply through the block education office / KGBV admissions notice.",
  "https://education.gov.in/", tg=["Student", "Girl child"], gender="Female", area="Rural", conf="medium", note=V16)

S("jnv", "Jawahar Navodaya Vidyalaya (JNV) Admission", MOE, EDU,
  "Free residential co-educational schools for talented rural children, admission via the JNVST entrance test for class 6.",
  "Free education, boarding, lodging and uniforms up to class 12; migration between regions.",
  "Children studying in class 5 in a government/aided recognised school in the district where they apply (at least 75% of seats reserved for rural candidates; reservations for girls, SC/ST, PwD).",
  ["Aadhaar", "Birth certificate", "Class 5 study certificate", "Category certificate (if any)", "Rural-area certificate (if applicable)"],
  "Apply online for JNVST on the Navodaya Vidyalaya Samiti portal during the notified window.",
  "https://navodaya.gov.in/", tg=["Student"], age_min=9, age_max=13, conf="medium")

S("nmmss", "National Means-cum-Merit Scholarship Scheme (NMMSS)", MOE, EDU,
  "Scholarship to prevent dropout of meritorious students from economically weaker families at class 8.",
  "₹12,000 per year for classes 9–12.",
  "Class 8 pass students (at least 55% marks; 50% for SC/ST) selected through a state-level exam, studying in government/aided schools; parental income up to ₹3.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], inc_max=350000, conf="medium", note=V16)

S("csss", "Central Sector Scheme of Scholarship for College and University Students (CSSS)", MOE, EDU,
  "Merit-based scholarship for college and university students from lower-income families.",
  "About ₹12,000 per year for graduation (first three years) and ₹20,000 per year for postgraduation.",
  "Students above the 80th percentile in the class 12 board exam, pursuing regular degree courses; family income up to ₹4.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], inc_max=450000, conf="medium", note=V16)

S("aicte-pragati", "AICTE Pragati Scholarship for Girl Students (Technical Education)", "AICTE (Ministry of Education)", EDU,
  "Scholarship to girl students in AICTE-approved technical degree and diploma courses.",
  "About ₹50,000 per year (tuition plus incidentals) for up to 4 years (3 for diploma/lateral entry).",
  "Girl students admitted to first year of AICTE-approved degree/diploma; family income up to ₹8 lakh; maximum two girl children per family.",
  NSP_DOCS[:1] + ["Income certificate", "Admission proof", "Marksheet", "Bank account"],
  NSP_HOW, NSP, tg=["Student", "Girl child"], gender="Female", inc_max=800000, conf="medium", note=V16)

S("aicte-saksham", "AICTE Saksham Scholarship for Differently-Abled Students", "AICTE (Ministry of Education)", EDU,
  "Scholarship for students with disabilities in AICTE-approved technical courses.",
  "About ₹50,000 per year for tuition and incidental expenses.",
  "Students with 40%+ disability admitted to AICTE-approved degree/diploma courses; family income up to ₹8 lakh.",
  NSP_DOCS[:1] + ["Disability certificate / UDID", "Income certificate", "Admission proof", "Bank account"],
  NSP_HOW, NSP, tg=["Student", "Person with disability"], inc_max=800000, conf="medium", note=V16)

S("pm-vidyalaxmi", "PM-Vidyalaxmi (Collateral-free Education Loans)", MOE, EDU,
  "Collateral-free, guarantor-free education loans for students admitted to top-ranked higher-education institutions.",
  "Loans with credit guarantee (about 75% for loans up to ₹7.5 lakh) and interest subvention (3% on loans up to ₹10 lakh for family income up to ₹8 lakh; full subvention for lower-income families not on other scholarships).",
  "Students admitted to Quality Higher Education Institutions (QHEIs) notified by the ministry.",
  ["Aadhaar", "Admission letter", "Income certificate", "Academic records", "Bank KYC"],
  "Apply through the PM-Vidyalaxmi portal; banks process the loan.",
  "https://pmvidyalaxmi.co.in/", tg=["Student"], conf="medium", note="Interest-subvention tiers and covered institutions are updated periodically.")

S("pmrf", "Prime Minister's Research Fellowship (PMRF)", MOE, EDU,
  "Fellowship for top students to pursue PhD at leading institutions.",
  "Monthly fellowship (roughly ₹70,000–₹80,000) plus annual research grant for up to 5 years.",
  "Bachelor's/master's graduates admitted to PhD at IITs, IISc, IISERs, NITs and other selected institutions, selected through the PMRF process.",
  ["Academic records", "GATE/NET score (as applicable)", "Research proposal", "Admission proof"],
  "Apply on the PMRF portal during the announced windows.",
  "https://www.pmrf.in/", tg=["Student", "Researcher"], conf="medium", note=V16)

S("inspire-she", "INSPIRE Scholarship for Higher Education (SHE)", "Dept. of Science & Technology", EDU,
  "Scholarship for meritorious students pursuing natural/basic sciences at UG and integrated MSc level.",
  "About ₹80,000 per year (scholarship plus mentorship grant) for up to 5 years.",
  "Students in the top 1% in class 12 boards or with top JEE/NEET/other exam ranks, studying B.Sc./B.S./Int. M.Sc. in natural and basic sciences.",
  ["Aadhaar", "Class 12 marksheet", "Admission proof", "Bank account"],
  "Apply on the INSPIRE portal in the annual window.",
  "https://online-inspire.gov.in/", tg=["Student"], conf="medium", note=V16)

S("inspire-manak", "INSPIRE Awards – MANAK", "Dept. of Science & Technology / NIF", EDU,
  "Programme to nurture creativity and innovation among school students (classes 6–10).",
  "₹10,000 award to selected students for developing ideas/models.",
  "Students of classes 6–10, nominated by their schools (one to a few nominations per school).",
  ["School nomination", "Aadhaar of student", "Bank account"],
  "Schools submit nominations on the MANAK portal.",
  "https://www.inspireawards-dst.gov.in/", tg=["Student"], age_min=10, age_max=15, conf="medium")

S("ishan-uday", "Ishan Uday – Special Scholarship for North Eastern Region Students", "University Grants Commission", EDU,
  "Scholarship for NER students pursuing general degree, technical or professional courses.",
  "Monthly scholarship (about ₹5,400 for general degree and ₹7,800 for technical/professional courses).",
  "Students domiciled in North Eastern states, pursuing regular UG courses in eligible institutions; family income up to ₹4.5 lakh per year.",
  NSP_DOCS, NSP_HOW, NSP, tg=["Student"], inc_max=450000, conf="medium", note=V16)

S("ugc-single-girl", "UGC Indira Gandhi Scholarship for Single Girl Child (PG)", "University Grants Commission", EDU,
  "Scholarship for the only girl child of the parents pursuing postgraduate courses.",
  "About ₹36,200 per month for two years.",
  "Single girl child of the family, aged up to 30, enrolled in regular full-time PG course.",
  ["Single girl child certificate/affidavit", "Aadhaar", "Admission proof", "Marksheets", "Bank account"],
  "Apply through the UGC scholarship portal / NSP as notified.",
  "https://www.ugc.gov.in/", tg=["Student", "Girl child"], gender="Female", age_max=30, conf="medium", note=V16)

S("swayam", "SWAYAM – Free Online Courses", MOE, EDU,
  "National platform offering free online courses from school level to postgraduate.",
  "Free access to courses; optional paid proctored exam and certificate.",
  "Any learner; no eligibility restriction.",
  ["Email / mobile number"],
  "Create a free account on the SWAYAM portal and enrol in courses.",
  "https://swayam.gov.in/", tg=["Student", "Learner"])

S("pmss-ex-servicemen", "Prime Minister's Scholarship Scheme (PMSS) for Wards of Ex-Servicemen and CAPF", "Kendriya Sainik Board / Ministry of Defence", EDU,
  "Scholarship for children and widows of ex-servicemen, Coast Guard, and central armed police forces personnel for technical/professional degrees.",
  "About ₹3,000 per month for boys and ₹3,600 per month for girls.",
  "Wards/widows of ex-servicemen and eligible CAPF/Rashtriya Rifles personnel with at least 60% marks in class 12, in eligible professional courses.",
  ["Discharge book / ex-servicemen identity", "Marksheets", "Admission proof", "Bank account"],
  "Apply on the Kendriya Sainik Board portal during the annual window.",
  "https://ksb.gov.in/", tg=["Student", "Ex-servicemen family"], conf="medium", note=V16)

# ---------- Health ----------
S("pmjay", "Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (PM-JAY)", NHA, HEA,
  "World's largest publicly funded health-assurance scheme covering secondary and tertiary hospitalisation.",
  "Cashless cover of ₹5 lakh per family per year at empanelled public and private hospitals.",
  "Poor and vulnerable families identified through SECC 2011 deprivation criteria and occupational categories (rural and urban); no cap on family size or age. Some states extend coverage further.",
  ["Aadhaar", "Ration card / identity proof", "Family details"],
  "Check eligibility on the PM-JAY portal/helpline 14555 and get an Ayushman card through a CSC, empanelled hospital or the Ayushman app.",
  "https://pmjay.gov.in/", tg=["Poor household"])

S("ab-vay-vandana", "Ayushman Vay Vandana Card (PM-JAY for Senior Citizens 70+)", NHA, HEA,
  "Extension of PM-JAY covering all senior citizens aged 70 and above irrespective of income.",
  "Health cover of ₹5 lakh per family per year (shared among 70+ members of the family); additional top-up for those already covered.",
  "All Indian citizens aged 70 and above, regardless of income; those covered under CGHS/ECHS/other public schemes may choose one.",
  ["Aadhaar", "Age proof"],
  "Enrol on the Ayushman Bharat beneficiary portal / Ayushman app or at a CSC.",
  "https://beneficiary.nha.gov.in/", tg=["Senior citizen"], age_min=70)

S("abdm", "Ayushman Bharat Digital Mission – ABHA Health ID", NHA, HEA,
  "Free 14-digit ABHA number and health account to store and share medical records digitally.",
  "Digital health ID, linkage of records across hospitals and labs, and paperless care.",
  "Any Indian resident.",
  ["Aadhaar or mobile number / driving licence"],
  "Create an ABHA number on the ABDM portal, ABHA app or at a participating facility.",
  "https://abha.abdm.gov.in/", tg=["Citizen"])

S("jan-aushadhi", "Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP)", "Dept. of Pharmaceuticals", HEA,
  "Network of Jan Aushadhi Kendras selling quality generic medicines at low prices.",
  "Medicines at prices commonly 50–80% lower than branded equivalents; entrepreneurs can open a Kendra with incentives.",
  "Any person can buy; individuals, doctors, pharmacists, NGOs and institutions can apply to open a Kendra.",
  ["Pharmacist registration / drug licence (for a Kendra)", "Aadhaar", "PAN", "Premises proof"],
  "Buy at any Kendra; apply to open one on the PMBJP portal.",
  "https://janaushadhi.gov.in/", tg=["Patient", "Entrepreneur"])

S("nikshay-poshan", "Ni-kshay Poshan Yojana (Nutritional Support for TB Patients)", MOHFW, HEA,
  "Monthly nutrition support to notified tuberculosis patients during treatment.",
  "₹1,000 per month via DBT for the duration of treatment (raised from ₹500 in 2024).",
  "TB patients notified on the Ni-kshay portal and on treatment.",
  ["Aadhaar", "Bank account", "TB notification"],
  "Enrol through the treating health facility/ASHA; the benefit is credited by DBT.",
  "https://nikshay.in/", tg=["Patient"], conf="medium", note="Confirm current monthly amount with the local TB officer.")

S("jsy", "Janani Suraksha Yojana (JSY)", MOHFW, HEA,
  "Cash assistance to promote institutional deliveries and reduce maternal and infant deaths.",
  "Cash incentive for institutional delivery (higher in low-performing states: about ₹1,400 rural / ₹1,000 urban).",
  "Pregnant women delivering in public/accredited facilities – all women in low-performing states; BPL/SC/ST women in other states.",
  ["Aadhaar", "JSY/MCP card", "Bank account", "BPL/caste certificate (where required)"],
  "Register at the nearest health centre / ASHA worker.",
  "https://nhm.gov.in/", tg=["Pregnant woman"], gender="Female", conf="medium", note=V16)

S("jssk", "Janani Shishu Suraksha Karyakram (JSSK)", MOHFW, HEA,
  "Free entitlements for pregnant women and sick newborns in public health facilities.",
  "Free delivery including caesarean, drugs, diagnostics, diet, blood and transport.",
  "All pregnant women delivering in public facilities and sick infants up to one year.",
  ["MCP card (helpful)"],
  "Visit a public health facility; contact the ASHA/ANM.",
  "https://nhm.gov.in/", tg=["Pregnant woman", "Infant"], gender="Female", conf="medium")

S("pmsma", "Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA)", MOHFW, HEA,
  "Free specialist antenatal check-up for pregnant women on the 9th of every month.",
  "Free antenatal check-ups, tests and high-risk pregnancy identification.",
  "Pregnant women in their second or third trimester.",
  ["MCP card"],
  "Visit a government health facility on the 9th of each month.",
  "https://pmsma.mohfw.gov.in/", tg=["Pregnant woman"], gender="Female", conf="medium")

S("rbsk", "Rashtriya Bal Swasthya Karyakram (RBSK)", MOHFW, HEA,
  "Free child-health screening and early intervention for defects at birth, deficiencies, diseases and developmental delays.",
  "Free screening, referral and treatment (including surgeries) for children aged 0–18 years.",
  "Children 0–18 years in the community, Anganwadis and government schools.",
  ["School/Anganwadi enrolment"],
  "Screening is done by mobile health teams at Anganwadis/schools; contact the district DEIC.",
  "https://nhm.gov.in/", tg=["Child"], age_max=18, conf="medium")

S("uip", "Universal Immunisation Programme (UIP)", MOHFW, HEA,
  "Free vaccination against vaccine-preventable diseases for children and pregnant women.",
  "Free vaccines including BCG, polio, DPT, measles-rubella, rotavirus, PCV and others per schedule.",
  "Infants, children and pregnant women.",
  ["MCP card / child immunisation card"],
  "Visit the nearest health centre/Anganwadi on immunisation days; register on the U-WIN app.",
  "https://nhm.gov.in/", tg=["Child", "Pregnant woman"])

S("e-sanjeevani", "eSanjeevani – National Telemedicine Service", MOHFW, HEA,
  "Free doctor-to-patient and doctor-to-doctor telemedicine.",
  "Free video/phone consultation and e-prescription.",
  "Any patient.",
  ["Mobile number"],
  "Register on the eSanjeevani portal/app or visit a Health & Wellness Centre.",
  "https://esanjeevani.mohfw.gov.in/", tg=["Patient"])

S("pm-dialysis", "Pradhan Mantri National Dialysis Programme", MOHFW, HEA,
  "Free dialysis services at district hospitals for poor patients.",
  "Free dialysis sessions for eligible patients.",
  "Patients with kidney failure below the poverty line; others may pay subsidised rates.",
  ["BPL card / identity proof", "Doctor's advice"],
  "Approach the dialysis unit at your district hospital.",
  "https://nhm.gov.in/", tg=["Patient", "BPL"], conf="medium")

S("ran", "Rashtriya Arogya Nidhi (RAN)", MOHFW, HEA,
  "Financial assistance to BPL patients for treatment of life-threatening diseases at government hospitals.",
  "One-time financial assistance towards treatment costs (ceiling as per scheme rules).",
  "Patients below the poverty line (as per the state BPL threshold) receiving treatment in specified government hospitals.",
  ["BPL/income certificate", "Medical estimate from the hospital", "Aadhaar"],
  "Apply through the medical superintendent of the government hospital.",
  "https://main.mohfw.gov.in/", tg=["Patient", "BPL"], conf="medium", note=V16)

S("echs", "Ex-Servicemen Contributory Health Scheme (ECHS)", "Ministry of Defence", HEA,
  "Cashless medical care for ex-servicemen pensioners and their dependants.",
  "Cashless treatment at ECHS polyclinics and empanelled hospitals.",
  "Ex-servicemen pensioners and dependants (one-time contribution based on rank).",
  ["Discharge book / PPO", "Identity proof", "Photographs", "Dependants' details"],
  "Apply at the nearest ECHS polyclinic or via the ECHS portal.",
  "https://echs.gov.in/", tg=["Ex-servicemen"], conf="medium")

# ---------- Skills & employment ----------
S("pmkvy", "Pradhan Mantri Kaushal Vikas Yojana (PMKVY 4.0)", MSDE, SKL,
  "Free short-term skill training with assessment and certification, plus placement support.",
  "Free training, NSQF-aligned certificate and job-placement assistance.",
  "Indian youth (school/college dropouts and unemployed) aged about 15–45 – see the Skill India portal for current age/course rules.",
  ["Aadhaar", "Educational documents", "Bank account"],
  "Register on the Skill India Digital portal and choose an accredited training centre.",
  "https://www.skillindiadigital.gov.in/", tg=["Youth", "Job seeker"], age_min=15, age_max=45, conf="medium",
  note="PMKVY 4.0 was approved to March 2026; confirm the current phase and open courses on Skill India Digital.")

S("naps", "National Apprenticeship Promotion Scheme (NAPS)", MSDE, SKL,
  "Supports employers in engaging apprentices by sharing part of the stipend and basic-training cost.",
  "Paid apprenticeship with certification; Government reimburses 25% of stipend (up to about ₹1,500 per month) to employers.",
  "Persons aged 14+ with the qualifications required for the trade; employers registered on the Apprenticeship portal.",
  ["Aadhaar", "Educational certificates", "Bank account"],
  "Register on the Apprenticeship India portal and apply to establishments offering apprenticeships.",
  "https://www.apprenticeshipindia.gov.in/", tg=["Youth", "Job seeker"], age_min=14, conf="medium", note=V16)

S("nats", "National Apprenticeship Training Scheme (NATS)", MOE, SKL,
  "Apprenticeship training for graduates, diploma holders and vocational-course pass-outs.",
  "On-the-job training with stipend; Government shares part of the stipend with the employer.",
  "Graduates, diploma and vocational-stream candidates seeking apprenticeship.",
  ["Aadhaar", "Educational certificates", "Bank account"],
  "Register on the NATS portal and apply to listed establishments.",
  "https://nats.education.gov.in/", tg=["Youth", "Job seeker"], conf="medium", note=V16)

S("ddu-gky", "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)", MORD, SKL,
  "Free residential/non-residential skilling and placement for poor rural youth.",
  "Free training, food/lodging, certification and placement support.",
  "Rural youth aged 15–35 from poor households (up to 45 for special categories such as persons with disability, PVTGs and women).",
  ["Aadhaar", "Educational documents", "BPL/poverty proof", "Bank account"],
  "Register on the DDU-GKY portal or contact a training partner/Block office.",
  "https://ddugky.gov.in/", tg=["Youth", "Job seeker"], age_min=15, age_max=35, area="Rural", conf="medium", note=V16)

S("rseti", "Rural Self-Employment Training Institutes (RSETI)", MORD, SKL,
  "Free short-term residential self-employment training with credit linkage, run by banks in each district.",
  "Free training (1–6 weeks), boarding/lodging and post-training handholding for loans.",
  "Rural youth aged 18–45, priority to BPL households, women and SC/ST candidates.",
  ["Aadhaar", "Passport photos", "BPL card (if applicable)", "Bank account"],
  "Contact your district RSETI (run by a lead bank) for upcoming batches.",
  "https://rural.gov.in/", tg=["Youth", "Job seeker"], age_min=18, age_max=45, area="Rural", conf="medium")

S("pm-internship", "PM Internship Scheme", "Ministry of Corporate Affairs", SKL,
  "12-month internships in top companies for young people to gain real-world experience.",
  "Monthly stipend of ₹5,000 (₹4,500 from Government + ₹500 from company), one-time ₹6,000 assistance and insurance cover.",
  "Indians aged 21–24 not in full-time employment or full-time education; family income up to ₹8 lakh; no family member in a regular government job; certain graduates (IIT/IIM/NLU/CA/MBBS etc.) excluded.",
  ["Aadhaar", "Educational certificates", "Bank account linked to Aadhaar", "Income self-declaration"],
  "Register on the PM Internship portal and apply to internship opportunities.",
  "https://pminternship.mca.gov.in/", tg=["Youth", "Job seeker"], age_min=21, age_max=24, inc_max=800000, conf="medium",
  note="Rollout is phased from a pilot; check the portal for current cycle and terms.")

S("ncs", "National Career Service (NCS) Portal", LAB, SKL,
  "Free national job-matching portal connecting job seekers, employers, training providers and career counsellors.",
  "Free registration, job matching, career counselling and skill-course listings.",
  "Any job seeker (special features for persons with disabilities, women and ex-servicemen).",
  ["Aadhaar / mobile number", "Educational and work details"],
  "Register on the NCS portal.",
  "https://www.ncs.gov.in/", tg=["Job seeker"])

S("skill-loan", "Skill Loan Scheme (Credit Guarantee Fund for Skill Development)", MSDE, SKL,
  "Bank loans to finance skill-training courses, backed by a credit-guarantee fund.",
  "Loans of about ₹5,000 to ₹1.5 lakh for training fees without collateral or third-party guarantee.",
  "Students/trainees admitted to eligible skill-development courses.",
  ["Aadhaar", "Admission/course proof", "Bank KYC"],
  "Apply at a participating bank or through the training provider linked to the scheme.",
  "https://www.nsdcindia.org/", tg=["Youth", "Student"], conf="medium", note=V16)

S("jss", "Jan Shikshan Sansthan (JSS)", MSDE, SKL,
  "Vocational training for non-literates, neo-literates and school dropouts, with focus on women and disadvantaged groups.",
  "Free or subsidised short-term vocational training.",
  "Persons aged about 15–45, priority to women, SC/ST and rural residents.",
  ["Aadhaar", "Educational details"],
  "Contact your district Jan Shikshan Sansthan.",
  "https://www.msde.gov.in/", tg=["Youth", "Woman"], age_min=15, age_max=45, conf="medium", note=V16)

S("my-bharat", "MY Bharat (Mera Yuva Bharat) Platform", "Ministry of Youth Affairs & Sports", SKL,
  "National youth platform for volunteering, internships, events and skilling opportunities.",
  "Access to volunteering, community programmes, learning and skilling opportunities.",
  "Young people aged 15–29.",
  ["Mobile number / Aadhaar"],
  "Register on the MY Bharat portal.",
  "https://mybharat.gov.in/", tg=["Youth"], age_min=15, age_max=29, conf="medium")

S("skill-india-digital", "Skill India Digital Hub (SIDH)", MSDE, SKL,
  "Digital platform for skilling, education and employment services in one place.",
  "Free course access, certification and job connect; single skill profile.",
  "Any learner or job seeker.",
  ["Aadhaar / DigiLocker login"],
  "Create a profile on the Skill India Digital portal.",
  "https://www.skillindiadigital.gov.in/", tg=["Youth", "Job seeker"])

# ---------- Sports & culture ----------
S("khelo-india-athlete", "Khelo India Scheme – Athlete Development", "Ministry of Youth Affairs & Sports", SPC,
  "Talent identification and long-term support to promising young athletes.",
  "Annual out-of-pocket allowance (about ₹10 lakh per athlete per year) for selected athletes, plus training and coaching support.",
  "Athletes selected via Khelo India Games/talent-identification processes.",
  ["Aadhaar", "Sports achievement records", "Bank account"],
  "Selection is through Khelo India Games/SAI processes; register on the Khelo India portal.",
  "https://kheloindia.gov.in/", tg=["Athlete", "Youth"], conf="medium", note=V16)

S("tops", "Target Olympic Podium Scheme (TOPS)", "Ministry of Youth Affairs & Sports", SPC,
  "Support to elite athletes with medal potential in Olympic/Paralympic cycles.",
  "Monthly out-of-pocket allowance, training/equipment and international exposure.",
  "Core and development-group athletes identified by the Mission Olympic Cell.",
  ["Athlete profile / achievements"],
  "Identification by the sports authority; no open application.",
  "https://www.sportsauthorityofindia.gov.in/", tg=["Athlete"], conf="medium", note=V16)

S("culture-artist-aid", "Financial Assistance to Needy Artists and Scholarships in Culture", "Ministry of Culture", SPC,
  "Pension/assistance for senior artistes and scholarships for young artistes in the arts.",
  "Monthly financial assistance for eligible senior artists; scholarships/fellowships for young talent.",
  "Practising artists/scholars meeting age, experience and income criteria of the specific component.",
  ["Aadhaar", "Proof of artistic career", "Age and income proof", "Bank account"],
  "Apply as per the Ministry of Culture notice/portal for the specific component.",
  "https://indiaculture.gov.in/", tg=["Artist"], conf="medium", note=V16)

MSME = "Ministry of MSME"
DFS = "Dept. of Financial Services"
MOHUA = "Ministry of Housing & Urban Affairs"
POST = "https://www.indiapost.gov.in/"
NSI = "https://www.nsiindia.gov.in/"
JSUR = "https://www.jansuraksha.gov.in/"

# ---------- Business & entrepreneurship ----------
S("mudra", "Pradhan Mantri MUDRA Yojana (PMMY)", DFS, BUS,
  "Collateral-free loans for micro and small non-farm enterprises.",
  "Loans in four bands: Shishu (up to ₹50,000), Kishor (₹50,001–₹5 lakh), Tarun (₹5–10 lakh) and Tarun Plus (up to ₹20 lakh for earlier good repayers).",
  "Indian citizens with a business plan for a non-farm income-generating activity in manufacturing, trading or services, including small shopkeepers, artisans, food processors and vendors.",
  ["Aadhaar", "PAN", "Business proof / plan", "Bank statements", "Address proof", "Passport photo"],
  "Apply at any bank, RRB, small finance bank or MFI, or through the Udyamimitra portal.",
  "https://www.mudra.org.in/", tg=["Entrepreneur", "Small business"], age_min=18)

S("pmegp", "Prime Minister's Employment Generation Programme (PMEGP)", MSME, BUS,
  "Credit-linked subsidy for setting up new micro-enterprises in manufacturing and services.",
  "Margin-money subsidy of 15–25% (general category, urban/rural) and 25–35% (special categories: SC/ST/OBC/minority/women/ex-servicemen/PwD/NER/hill and border areas) of the project cost.",
  "Individuals above 18, self-help groups, cooperatives and charitable trusts setting up new projects; project cost up to ₹50 lakh (manufacturing) or ₹20 lakh (service); minimum VIII pass for larger projects. No income ceiling.",
  ["Aadhaar", "PAN", "Project report", "Caste/special-category certificate (if applicable)", "Educational certificate", "Bank account"],
  "Apply online on the PMEGP e-portal; loans are sanctioned by banks with KVIC/KVIB/DIC support.",
  "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp", tg=["Entrepreneur", "Unemployed youth"], age_min=18, conf="medium", note=V16)

S("pm-vishwakarma", "PM Vishwakarma", MSME, BUS,
  "Support for traditional artisans and craftspeople across 18 trades (e.g., carpenter, blacksmith, potter, tailor, cobbler, mason, barber, washerman, goldsmith).",
  "PM Vishwakarma certificate/ID, skill training with ₹500/day stipend, ₹15,000 toolkit incentive, collateral-free loans (₹1 lakh then ₹2 lakh at 5% interest) and digital-transaction incentives.",
  "Artisans and craftspeople aged 18+ working with hands and tools in one of the 18 trades; not availing similar credit schemes (PMEGP/PM SVANidhi/Mudra) in the last 5 years; one member per family; government employees and their families excluded.",
  ["Aadhaar (with mobile linked)", "Bank account", "Ration card", "Trade proof / self-declaration"],
  "Register at a CSC with biometric Aadhaar authentication on the PM Vishwakarma portal; verified by Gram Panchayat/ULB and district committee.",
  "https://pmvishwakarma.gov.in/", tg=["Artisan"], age_min=18, conf="medium", note="Scheme runs to FY 2027-28; confirm current terms on the portal.")

S("pm-svanidhi", "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)", MOHUA, BUS,
  "Working-capital loans for street vendors to restart and grow their business.",
  "Collateral-free loans in three tiers (₹15,000, then ₹25,000, then ₹50,000) with interest subsidy on timely repayment and cashback for digital payments (restructured version extended to 2030).",
  "Street vendors with a certificate of vending/identity card or letter of recommendation from the urban local body.",
  ["Aadhaar", "Vending certificate / ID card / LoR", "Bank account", "Mobile number"],
  "Apply on the PM SVANidhi portal or through a bank/CSC with ULB verification.",
  "https://pmsvanidhi.mohua.gov.in/", tg=["Street vendor"], area="Urban", conf="medium",
  note="Loan tiers revised in 2025; confirm current amounts on the portal.")

S("sisfs", "Startup India Seed Fund Scheme (SISFS)", "DPIIT (Ministry of Commerce & Industry)", BUS,
  "Financial assistance to early-stage startups for proof of concept, prototype, trials and market entry via incubators.",
  "Grants up to ₹20 lakh for validation/prototype and investment up to ₹50 lakh via convertible debentures/debt instruments, routed through selected incubators.",
  "DPIIT-recognised startups incorporated less than 2 years ago that have not received more than ₹10 lakh of other government support.",
  ["DPIIT recognition certificate", "Incorporation documents", "Pitch deck / business plan", "Founders' KYC"],
  "Apply to a selected incubator through the Startup India portal.",
  "https://seedfund.startupindia.gov.in/", tg=["Startup founder"], conf="medium", note=V16)

S("startup-recognition", "Startup India – DPIIT Recognition and Benefits", "DPIIT (Ministry of Commerce & Industry)", BUS,
  "Recognition for eligible startups, unlocking tax benefits, easier compliance and access to government support.",
  "Eligibility for income-tax exemption (Section 80-IAC, subject to approval), self-certification compliance, fast-track patent examination and access to funding schemes.",
  "Entities incorporated as a private limited company, LLP or registered partnership, less than 10 years old, with turnover below ₹100 crore, working on innovation or scalable business models.",
  ["Incorporation certificate", "Description of innovation / business", "Founders' PAN/Aadhaar"],
  "Register and apply for recognition on the Startup India portal.",
  "https://www.startupindia.gov.in/", tg=["Startup founder"], conf="medium", note="Age/turnover thresholds were revised in 2025; confirm on the portal.")

S("cgtmse", "Credit Guarantee Scheme for Micro and Small Enterprises (CGTMSE)", MSME + " / SIDBI", BUS,
  "Collateral-free credit guarantee cover to lenders for loans to micro and small enterprises.",
  "Collateral- and third-party-guarantee-free loans; guarantee cover from the Credit Guarantee Fund Trust.",
  "New and existing micro and small enterprises (manufacturing and services), including women entrepreneurs, through member lending institutions.",
  ["Udyam registration", "PAN", "Project report / financials", "Bank KYC"],
  "Apply for a business loan at a participating bank/NBFC; the lender obtains CGTMSE cover.",
  "https://www.cgtmse.in/", tg=["Entrepreneur"], conf="medium", note="Guarantee-cover limits were revised in 2025; check with the lender.")

S("udyam", "Udyam Registration (MSME Registration)", MSME, BUS,
  "Free online registration for micro, small and medium enterprises, needed to access many MSME benefits.",
  "Udyam certificate/number enabling priority-sector lending, collateral-free loans, subsidies, protection against delayed payments and eligibility for government tenders.",
  "Any business meeting the current MSME investment and turnover limits (micro, small or medium).",
  ["Aadhaar of proprietor/partner/director", "PAN", "GSTIN (if applicable)", "Bank account details"],
  "Register free on the Udyam Registration portal.",
  "https://udyamregistration.gov.in/", tg=["Entrepreneur", "Small business"])

S("nsic", "NSIC Support Schemes for Small Enterprises", "National Small Industries Corporation (MSME)", BUS,
  "Raw-material assistance, marketing support, single-point registration for government purchases and credit support for small enterprises.",
  "Help with raw-material purchase, tender participation benefits, bill discounting and marketing assistance.",
  "Micro and small enterprises registered on Udyam.",
  ["Udyam registration", "PAN", "GST details", "Financial statements"],
  "Register through the NSIC portal or nearest NSIC office.",
  "https://www.nsic.co.in/", tg=["Entrepreneur"], conf="medium")

S("zed", "MSME Sustainable (ZED) Certification Scheme", MSME, BUS,
  "Zero Defect Zero Effect certification to improve quality and reduce environmental impact of MSMEs.",
  "Subsidy on certification cost (higher for micro and small units; extra for women/SC/ST-owned) and handholding support.",
  "Udyam-registered micro, small and medium enterprises.",
  ["Udyam registration", "Business/quality details"],
  "Register and apply on the ZED portal.",
  "https://zed.msme.gov.in/", tg=["Entrepreneur"], conf="medium", note=V16)

S("pmfme", "PM Formalisation of Micro Food Processing Enterprises (PMFME)", "Ministry of Food Processing Industries", BUS,
  "Support to upgrade and formalise micro food-processing units.",
  "Credit-linked capital subsidy of 35% (up to ₹10 lakh per unit), seed capital for SHG members (about ₹40,000) and training/branding support.",
  "Existing individual micro food-processing units, FPOs, SHGs and cooperatives.",
  ["Aadhaar", "Udyam/GST or business proof", "Project details", "Bank account"],
  "Apply on the PMFME portal / through the District Resource Person.",
  "https://pmfme.mofpi.gov.in/", tg=["Entrepreneur", "SHG member"], conf="medium", note=V16)

S("mahila-e-haat", "Mahila E-Haat", WCD if False else "Ministry of Women & Child Development", BUS,
  "Online marketing platform for women entrepreneurs, SHGs and NGOs to display and sell products.",
  "Free online marketplace listing and marketing support.",
  "Women entrepreneurs, SHGs and NGOs.",
  ["Aadhaar", "Bank account", "Product details"],
  "Register on the Mahila E-Haat portal.",
  "https://mahilaehaat-rmk.gov.in/", tg=["Woman entrepreneur", "SHG member"], gender="Female", conf="medium")

S("ahvy", "Ambedkar Hastshilp Vikas Yojana (National Handicraft Development)", "Development Commissioner (Handicrafts), Ministry of Textiles", BUS,
  "Support for handicraft artisans through design, technology upgrade, training and marketing.",
  "Skill and design training, tool kits, marketing assistance and exhibitions for artisans.",
  "Handicraft artisans with an Artisan (Pehchan) ID card and artisan groups/cooperatives.",
  ["Artisan ID card", "Aadhaar", "Bank account"],
  "Apply through the Development Commissioner (Handicrafts) offices or the portal.",
  "https://handicrafts.nic.in/", tg=["Artisan"], conf="medium", note=V16)

S("nhdp", "National Handloom Development Programme (NHDP)", "Ministry of Textiles", BUS,
  "Support for handloom weavers with looms, yarn, design and marketing help.",
  "Assistance for looms and accessories, yarn supply at subsidised rates, design support, and access to Weavers' Mudra loans.",
  "Handloom weavers and workers with a Handloom Weaver ID / Pehchan card and weaver groups.",
  ["Weaver ID card", "Aadhaar", "Bank account"],
  "Apply through the Handloom Development Commissioner office / state handloom department.",
  "https://handlooms.nic.in/", tg=["Weaver", "Artisan"], conf="medium", note=V16)

S("day-nulm", "DAY-NULM (Urban Livelihoods Mission)", MOHUA, SKL,
  "Skill training, SHG formation and self-employment loans for the urban poor.",
  "Free skill training, interest subsidy on bank loans for self-employment, and shelter/vendor support for eligible urban poor.",
  "Urban poor households, SHG members, street vendors and unemployed youth in cities and towns.",
  ["Aadhaar", "Address proof", "Income/BPL proof", "Bank account"],
  "Apply through your urban local body's NULM cell.",
  "https://nulm.gov.in/", tg=["Urban poor", "SHG member"], area="Urban", conf="medium", note=V16)

# ---------- Banking, insurance, pensions, savings ----------
S("pmjdy", "Pradhan Mantri Jan Dhan Yojana (PMJDY)", DFS, BFI,
  "National mission for universal access to banking through zero-balance basic savings accounts.",
  "Zero-balance account, RuPay debit card with ₹2 lakh accident insurance (for cards issued after 28 Aug 2018), overdraft facility up to ₹10,000 and DBT eligibility.",
  "Any Indian citizen aged 10+ who does not have a bank account.",
  ["Aadhaar or other officially valid document", "Passport photo"],
  "Open an account at any bank branch or through a Business Correspondent.",
  "https://pmjdy.gov.in/", tg=["Citizen", "Unbanked"], age_min=10)

S("pmjjby", "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)", DFS, BFI,
  "Low-cost renewable life-insurance cover.",
  "₹2 lakh life cover for death from any cause; premium about ₹436 per year auto-debited.",
  "Bank/post-office account holders aged 18–50 (cover continues to age 55).",
  ["Aadhaar", "Savings bank account", "Consent for auto-debit"],
  "Enrol through your bank/post office or net-banking; renew annually.",
  JSUR, tg=["Citizen"], age_min=18, age_max=50, conf="medium", note="Premium is revised occasionally; confirm with your bank.")

S("pmsby", "Pradhan Mantri Suraksha Bima Yojana (PMSBY)", DFS, BFI,
  "Low-cost accident insurance cover.",
  "₹2 lakh for accidental death or total permanent disability and ₹1 lakh for partial disability; premium about ₹20 per year.",
  "Bank/post-office account holders aged 18–70.",
  ["Aadhaar", "Savings bank account", "Consent for auto-debit"],
  "Enrol through your bank/post office or net-banking; renew annually.",
  JSUR, tg=["Citizen"], age_min=18, age_max=70, conf="medium", note="Premium is revised occasionally; confirm with your bank.")

S("apy", "Atal Pension Yojana (APY)", DFS + " / PFRDA", BFI,
  "Guaranteed pension scheme for citizens, especially unorganised-sector workers.",
  "Fixed monthly pension of ₹1,000–₹5,000 after age 60 depending on contribution; nominee gets the corpus.",
  "Indian citizens aged 18–40 with a bank/post-office savings account; income-tax payers are not eligible.",
  ["Aadhaar", "Savings bank account", "Mobile number", "Nominee details"],
  "Enrol at your bank branch or through net-banking/mobile banking.",
  JSUR, tg=["Citizen", "Unorganised worker"], age_min=18, age_max=40, conf="medium", note=V16)

S("nps", "National Pension System (NPS)", "PFRDA", BFI,
  "Voluntary long-term retirement savings and pension account open to all citizens.",
  "Market-linked retirement corpus with tax benefits; partial withdrawal and annuity options.",
  "Indian citizens (resident and NRI) aged 18–70.",
  ["Aadhaar or PAN", "Bank account", "Nominee details"],
  "Open an NPS account online via eNPS or through a Point of Presence (bank/post office).",
  "https://enps.nsdl.com/", tg=["Citizen"], age_min=18, age_max=70)

S("nps-vatsalya", "NPS Vatsalya", "PFRDA", BFI,
  "Pension account for minors, opened and managed by parents/guardians.",
  "Long-term savings for a child that converts to a regular NPS account at age 18.",
  "Parents/guardians of Indian minors below 18 years; minimum contribution about ₹1,000 per year.",
  ["Child's birth proof", "Parent/guardian KYC", "Bank account"],
  "Open online via eNPS or at a Point of Presence.",
  "https://www.pfrda.org.in/", tg=["Child", "Parent"], age_max=18, conf="medium", note="Check contribution rules on the PFRDA site.")

S("ups", "Unified Pension Scheme (UPS) for Central Government Employees", "Dept. of Financial Services / PFRDA", BFI,
  "Assured-payout pension option for central government employees, available from 1 April 2025.",
  "Assured pension linked to average basic pay (about 50% of the last 12 months' average for 25 years of qualifying service), with family pension and minimum pension assurance.",
  "Central government employees covered by NPS who opt for UPS, and eligible retirees as notified.",
  ["Service records", "Option form", "Employee KYC"],
  "Opt in through your Drawing & Disbursing Officer / NPS portal as notified.",
  "https://www.pfrda.org.in/", tg=["Government employee"], conf="medium", note="Check the latest option deadlines and rules with your department.")

S("ssy", "Sukanya Samriddhi Yojana (SSY)", DFS, BFI,
  "Small-savings account for the girl child with a government-notified interest rate and tax benefits.",
  "Interest-bearing account (rate reset quarterly), tax benefits, maturity after 21 years; partial withdrawal for education/marriage after age 18.",
  "Parents/guardians of a girl child below 10 years; up to two accounts per family (three if twins/triplets).",
  ["Girl's birth certificate", "Guardian's ID and address proof", "Initial deposit (minimum ₹250)"],
  "Open at any post office or authorised bank; deposit ₹250–₹1.5 lakh per year for 15 years.",
  NSI, tg=["Girl child", "Parent"], gender="Female", age_max=10, area="Both")

S("ppf", "Public Provident Fund (PPF)", DFS, BFI,
  "Long-term tax-advantaged savings scheme with a government-notified interest rate.",
  "15-year account with tax benefits and interest set quarterly; deposits ₹500–₹1.5 lakh per year.",
  "Any resident Indian individual (one account per person); parents can open for a minor.",
  ["Aadhaar/PAN", "Address proof", "Passport photo", "Nomination form"],
  "Open at any post office or authorised bank.",
  NSI, tg=["Citizen"])

S("scss", "Senior Citizens' Savings Scheme (SCSS)", DFS, BFI,
  "Government savings scheme for seniors with quarterly interest payouts.",
  "5-year deposit (extendable by 3 years) with quarterly interest; maximum deposit ₹30 lakh.",
  "Persons aged 60+ (55–60 for those retired under superannuation/VRS; 50–60 for retired defence personnel).",
  ["Age proof", "Retirement proof (if under 60)", "Aadhaar/PAN", "Passport photo"],
  "Open at any post office or authorised bank.",
  NSI, tg=["Senior citizen"], age_min=55)

S("pomis", "Post Office Monthly Income Scheme (POMIS)", DFS, BFI,
  "Post-office deposit that pays fixed interest every month.",
  "5-year deposit with monthly interest payout; maximum ₹9 lakh (single) or ₹15 lakh (joint).",
  "Resident Indian adults; parents can open for minors.",
  ["Aadhaar/PAN", "Address proof", "Passport photo"],
  "Open at any post office.",
  POST, tg=["Citizen"], age_min=18)

S("nsc", "National Savings Certificate (NSC VIII Issue)", DFS, BFI,
  "Fixed-income savings certificate sold by post offices.",
  "5-year certificate with compounding interest and tax benefits; minimum ₹1,000, no maximum limit.",
  "Resident Indian individuals; guardians can buy for minors.",
  ["Aadhaar/PAN", "Address proof", "Passport photo"],
  "Buy at any post office.",
  POST, tg=["Citizen"])

S("kvp", "Kisan Vikas Patra (KVP)", DFS, BFI,
  "Post-office savings certificate that doubles the investment over a fixed period.",
  "Investment doubles in about 115 months (at the current rate); minimum ₹1,000, no maximum.",
  "Resident Indian adults; guardians can buy for minors.",
  ["Aadhaar/PAN", "Address proof", "Passport photo"],
  "Buy at any post office.",
  POST, tg=["Citizen"])

# ---------- Housing ----------
S("pmay-g", "Pradhan Mantri Awas Yojana – Gramin (PMAY-G)", MORD if False else "Ministry of Rural Development", HOU,
  "Assistance to build a pucca house with basic amenities for eligible rural households.",
  "₹1.2 lakh (plains) or ₹1.3 lakh (hilly/difficult/NER) per house, plus ₹12,000 for toilet under SBM-G and 90/95 person-days of wage employment.",
  "Rural households that are houseless or live in kutcha/dilapidated houses, identified through SECC/Awaas+ survey; revised exclusion criteria (2024) apply, including a household income limit of about ₹15,000 per month.",
  ["Aadhaar", "Bank account", "Job card (if any)", "Land/homestead proof"],
  "Beneficiaries are identified via the Awaas+ survey through the Gram Panchayat; use the PMAY-G portal/app for self-survey where enabled.",
  "https://pmayg.nic.in/", tg=["Household", "Rural poor"], area="Rural", inc_max=180000,
  inc_note="Monthly household income about ₹15,000 (revised Awaas+ norms)", conf="medium",
  note="Extended to March 2029 for 2 crore additional houses; confirm current norms on the portal.")

S("pmay-u-blc", "PMAY-Urban 2.0 – Beneficiary-Led Construction (BLC)", MOHUA, HOU,
  "Central assistance to build/enhance a house on own land for eligible urban households.",
  "Central assistance of about ₹2.5 lakh per house.",
  "EWS (income up to ₹3 lakh), LIG (₹3–6 lakh) and MIG (₹6–9 lakh) urban households not owning a pucca house anywhere in India, with the woman as owner/co-owner where possible.",
  ["Aadhaar", "Income certificate", "Land/ownership documents", "Bank account", "Self-declaration of no pucca house"],
  "Apply through your urban local body / the PMAY-Urban 2.0 portal.",
  "https://pmay-urban.gov.in/", tg=["Household"], area="Urban", inc_max=900000, conf="medium", note=V16)

S("pmay-u-iss", "PMAY-Urban 2.0 – Interest Subsidy Scheme (ISS)", MOHUA, HOU,
  "Interest subsidy on home loans for buying or building a house.",
  "Interest subsidy of 4% on home loans up to ₹8 lakh for up to 12 years (maximum subsidy about ₹1.8 lakh).",
  "EWS/LIG/MIG urban households (income up to ₹9 lakh) not owning a pucca house, taking a home loan for a house of eligible value.",
  ["Aadhaar", "Income proof", "Home-loan sanction letter", "Property documents", "Self-declaration of no pucca house"],
  "Apply through the lending institution (bank/HFC) registered under the scheme.",
  "https://pmay-urban.gov.in/", tg=["Household", "Home buyer"], area="Urban", inc_max=900000, conf="medium", note=V16)

S("pmay-u-ahp", "PMAY-Urban 2.0 – Affordable Housing in Partnership (AHP)", MOHUA, HOU,
  "Central assistance for EWS houses built in partnership with states, ULBs or private developers.",
  "Central assistance of about ₹2.5 lakh per EWS house.",
  "EWS urban households (income up to ₹3 lakh) not owning a pucca house.",
  ["Aadhaar", "Income certificate", "Self-declaration of no pucca house"],
  "Apply through the ULB or the developer's project under the scheme.",
  "https://pmay-urban.gov.in/", tg=["Household"], area="Urban", inc_max=300000, conf="medium", note=V16)

S("pmay-u-arh", "PMAY-Urban 2.0 – Affordable Rental Housing (ARH)", MOHUA, HOU,
  "Affordable rental housing for urban migrants, workers and students.",
  "Rental housing units at affordable rents in ARHC projects.",
  "Urban migrants/workers, students and the urban poor.",
  ["Aadhaar", "Employment/student proof"],
  "Apply through the ARHC project manager / ULB.",
  "https://pmay-urban.gov.in/", tg=["Migrant worker", "Student"], area="Urban", conf="medium", note=V16)

# ---------- Energy & utilities ----------
S("pmuy", "Pradhan Mantri Ujjwala Yojana (PMUY)", "Ministry of Petroleum & Natural Gas", UTL,
  "Free LPG connections for poor women to move households to clean cooking fuel.",
  "Deposit-free LPG connection (financial support for connection, stove and first refill); targeted subsidy on refills (₹300 per 14.2 kg cylinder for up to 9 refills a year in recent years).",
  "Adult women from BPL and specified priority households (SC/ST, PMAY, AAY, forest dwellers, most backward classes, tea-garden workers, etc.) without an LPG connection in the household.",
  ["Aadhaar", "KYC application form", "Ration card / BPL proof", "Bank account", "Passport photo"],
  "Apply at an LPG distributor or on the PMUY portal.",
  "https://www.pmuy.gov.in/", tg=["Woman", "BPL"], gender="Female", age_min=18, conf="medium",
  note="Confirm whether the ₹300 refill subsidy has been extended for FY 2026-27.")

S("pm-surya-ghar", "PM Surya Ghar: Muft Bijli Yojana (Rooftop Solar)", "Ministry of New & Renewable Energy", UTL,
  "Rooftop solar for households to cut electricity bills and earn from surplus power.",
  "Central subsidy of ₹30,000 per kW for the first 2 kW and ₹18,000 for the 3rd kW (maximum ₹78,000), plus collateral-free low-interest loans.",
  "Indian households with a valid electricity connection and a suitable roof; not previously subsidised for rooftop solar.",
  ["Aadhaar", "Electricity bill", "Roof ownership/consent proof", "Bank account"],
  "Register on the PM Surya Ghar portal, pick a registered vendor, and get subsidy after commissioning.",
  "https://pmsuryaghar.gov.in/", tg=["Household"], conf="medium")

# ---------- Digital & communication ----------
S("csc-vle", "Common Service Centre (CSC) – Village Level Entrepreneur", "Ministry of Electronics & IT", SIT,
  "Programme to run a Common Service Centre delivering government and business services in villages and towns.",
  "Earn commission on services such as PAN, Aadhaar-related help, banking, insurance, bill payment and e-governance.",
  "Individuals (preferably with basic computer skills) who want to set up a CSC.",
  ["Aadhaar", "PAN", "Educational certificate", "Premises details", "Bank account"],
  "Register on the CSC portal and apply to become a VLE.",
  "https://csc.gov.in/", tg=["Entrepreneur", "Youth"], age_min=18, conf="medium")

S("pm-wani", "PM-WANI (Public Wi-Fi Network Interface)", "Dept. of Telecommunications", SIT,
  "Framework that lets small shops and entrepreneurs offer public Wi-Fi without a licence.",
  "No licence or registration fee to become a Public Data Office (PDO); earn revenue from data vouchers.",
  "Individuals, shopkeepers and small entrepreneurs with broadband access.",
  ["Aadhaar/PAN", "Business/premises proof", "Broadband connection details"],
  "Register with a Public Data Office Aggregator (PDOA) listed on the PM-WANI portal.",
  "https://pmwani.gov.in/", tg=["Entrepreneur"], conf="medium")

# ---------- Transport ----------
S("rail-divyang-concession", "Indian Railways Concessions for Divyangjan, Patients and Students", "Ministry of Railways", TRN,
  "Fare concessions for eligible categories of passengers.",
  "Percentage concession on fares (varies by category and class) for persons with disabilities, certain patients and students on eligible journeys.",
  "Persons with disabilities, patients with specified ailments and students meeting the prescribed conditions.",
  ["Disability certificate / UDID / medical certificate", "Identity proof", "Institution certificate (for students)"],
  "Obtain the concession certificate/ID as prescribed and book at the reservation counter or online with the eligible category.",
  "https://indianrailways.gov.in/", tg=["Person with disability", "Student", "Patient"], conf="medium",
  note="Concession categories and rates are revised by the Railway Board; check current rules.")

with open("d:/moneyfollows/backend/data/government_schemes_1200.json", "w", encoding="utf-8") as f:
    json.dump(schemes, f, indent=2, ensure_ascii=False)

report = {
  "total_records": len(schemes),
  "central_schemes": len(schemes),
  "state_schemes": 0,
  "states_covered": [],
  "categories": {},
  "gender_criteria": {},
  "income_criteria_count": 0,
  "age_criteria_count": 0,
  "education_criteria_count": 0,
  "occupation_criteria_count": 0,
  "direct_application_links": 0,
  "myscheme_links": 0,
  "records_without_direct_application_link": 0
}

with open("d:/moneyfollows/backend/data/dataset_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("Created government_schemes_1200.json with", len(schemes), "schemes.")
