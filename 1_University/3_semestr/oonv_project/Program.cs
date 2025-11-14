using oonv.bridge;

namespace oonv;
class Program
{
    static void Main(string[] args)
    {
        ZatutejATimPoslesBitcoin app = new ZatutejATimPoslesBitcoin();
        app.TutProPenize();
        TestBridge bridgeTest = new TestBridge();
        bridgeTest.TestMe();
    }
}