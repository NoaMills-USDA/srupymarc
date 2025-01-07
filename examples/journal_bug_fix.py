import srupymarc
import pymarc

url = "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST"
query_journal = 'alma.local_field_990="Journal repository"'
query_article = "alma.issn=1365-6937"
maximum_records = 1
sru_version = "1.2"
start_record = 8

params = {
    "url": url,
    "sru_version": sru_version,
    "query": query_journal,
    "start_record": start_record,
    "maximum_records": maximum_records,
}

records = srupymarc.searchretrieve(**params)

for i in range(10):
    print("Leader result: ", records[i].leader)