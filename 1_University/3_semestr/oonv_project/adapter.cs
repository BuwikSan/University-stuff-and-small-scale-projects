// Stará třída s nekompatibilním rozhraním

namespace oonv;

public interface ITutace
{
    void TutProPenize();
}

public interface IPaymentAPI
{
    double ConvertCurrency(double amount, string currency);
    void Transfer(double amount);
}

public class ZatutejATimPoslesBitcoin : ITutace
{
    private TutToBitcoinAdapter adapter = new TutToBitcoinAdapter();
    public void TutProPenize()
    {

        while (true)
        {
            Console.Write("Zadej příkaz ('tut' nebo 'konec'): ");
            string? input = Console.ReadLine();

            if (input?.ToLower() == "konec")
            {
                Console.WriteLine("Ukončuji...");
                break;
            }
            else if (input?.ToLower() == "tut")
            {
                Console.WriteLine("Tut tut! Posílám Bitcoin...");
                adapter.ProcessPayment();
            }
            else
            {
                Console.WriteLine("Neznámý příkaz!");
            }

            Console.WriteLine();
        }
    }
}

public class BitcoinAPI : IPaymentAPI
{
    public double ConvertCurrency(double amount, string currency)
    {
        if (currency == "USD") return amount / 4300;
        else if (currency == "EUR") return amount / 4200;
        else if (currency == "CZK") return amount / 4200 / 24;
        else throw new ArgumentException($"Unknown currency: {currency}");
    }

    public void Transfer(double amount)
    {
        if (amount <= 0)
        {
            // Další příklad výjimky
            throw new InvalidOperationException("Amount must be greater than zero");
        }

        Console.WriteLine($"Bitcoins were transferred: {amount:F8} BTC");
    }
}

public class TutToBitcoinAdapter
{
    private BitcoinAPI bitcoin = new BitcoinAPI();
    public void ProcessPayment()
    {
        bitcoin.Transfer(0.000000000001);
    }
}
