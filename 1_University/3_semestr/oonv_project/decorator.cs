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

// BaseDecorator should be an abstract class that implements Komponent
// and delegates to an inner Komponent. Concrete decorators extend this
// abstract class and override/extend behavior.
public abstract class BaseDecorator : Komponent
{
    private Komponent komponent;
    public BaseDecorator(Komponent komponent)
    {
        this.komponent = komponent;
    }

    // Default behavior: delegate to wrapped component.
    // Concrete decorators can override this if needed, or call base.udelejKafe().
    public virtual Kafe udelejKafe()
    {
        return komponent.udelejKafe();
    }

    // Concrete decorators must implement extra to augment the produced Kafe.
    public abstract Kafe extra(Kafe kafe);
}

// Example concrete decorator that adds "mleko" to the coffee
public class MlekoDecorator : BaseDecorator
{
    public MlekoDecorator(Komponent c) : base(c){}

    public override Kafe udelejKafe()
    {
        // get the base coffee from wrapped component
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

// Another example decorator that adds sugar
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