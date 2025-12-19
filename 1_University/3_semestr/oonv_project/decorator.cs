namespace oonv;

public class Kafe
{
    public List<string> propertyList = new List<string>();
    public Kafe(){}
}

public interface Komponent
{
    public Kafe udelejKafe();
}

public class Kavovar : Komponent
{
    public Kavovar(){}

    public Kafe udelejKafe()
    {
        Kafe kafe = new Kafe();
        return kafe;
    }

}
public abstract class BaseDecorator : Komponent
{
    private Komponent komponent;
    public BaseDecorator(Komponent komponent)
    {
        this.komponent = komponent;
    }

    public virtual Kafe udelejKafe()
    {
        return komponent.udelejKafe();
    }

    public abstract Kafe extra(Kafe kafe);
}

public class MlekoDecorator : BaseDecorator
{
    public MlekoDecorator(Komponent c) : base(c){}

    public override Kafe udelejKafe()
    {
        var k = base.udelejKafe();
        return extra(k);
    }

    public override Kafe extra(Kafe kafe)
    {
        if (kafe.propertyList == null) kafe.propertyList = new List<string>();
        kafe.propertyList.Add("mleko");
        return kafe;
    }
}

public class CukrDecorator : BaseDecorator
{
    public CukrDecorator(Komponent c) : base(c){}

    public override Kafe udelejKafe()
    {
        var k = base.udelejKafe();
        return extra(k);
    }

    public override Kafe extra(Kafe kafe)
    {
        if (kafe.propertyList == null) kafe.propertyList = new List<string>();
        kafe.propertyList.Add("cukr");
        return kafe;
    }
}