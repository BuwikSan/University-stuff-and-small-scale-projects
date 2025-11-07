namespace oonv;
interface Database
{
    public string ReadRecord();
    public string WriteRecord();
}

class MySQL : Database
{
    public MySQL() { }
    public string ReadRecord() { return "MySQL ReadRecord"; }
    public string WriteRecord() { return "MySQL WriteRecord"; }
}

class MongoDB : Database
{
    public MongoDB() { }
    public string ReadRecord() { return "MongoDB ReadRecord"; }
    public string WriteRecord() { return "MongoDB WriteRecord"; }
}

class Factory
{
    public Database CreateProduct(string typ)
    {
        if (typ == "NoSQL") { return new MongoDB(); }
        else { return new MySQL(); }
    }
}