namespace NavrhoveVzory;
interface Database
{
    public string ReadRecord();
    public void WriteRecord();
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

class Program
{
    static void Main(string[] args)
    {
        Factory tovarnickaNaDB = new Factory();
        Database db = tovarnickaNaDB.CreateProduct("SQL");
        Console.WriteLine(db.ReadRecord());
    }
}