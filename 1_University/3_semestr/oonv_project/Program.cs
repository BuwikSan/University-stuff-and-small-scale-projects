using oonv.bridge;

namespace oonv;
class Program
{
    static void Main(string[] args)
    {
        Komponent kavovar = new Kavovar();
        Komponent kavovarAMleko = new MlekoDecorator(kavovar);
        Komponent kavovarMlekoACukr = new CukrDecorator(kavovarAMleko);

        Kafe kaficko = kavovarMlekoACukr.udelejKafe();
        foreach (string vlastnost in kaficko.propertyList)
        {
            Console.WriteLine(vlastnost);
        }
    }
}