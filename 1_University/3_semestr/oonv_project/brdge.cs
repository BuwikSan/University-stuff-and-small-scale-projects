
using System.ComponentModel.DataAnnotations;
using System.Runtime.CompilerServices;

namespace oonv.bridge;

interface Device
{
    bool IsEnabled();
    void Enable();
    void Disable();
    void SetVolume(int newVolume);
    int GetVolume();
    int GetMaxVolume();
    void SetChannel(int newChannel);
    int GetChannel();
    int GetNumOfChannels();

}

abstract class Remote
{
    private Device _device;
    public Remote(Device device)
    {
        _device = device;
    }

    public void TogglePower()
    {
        if (_device.IsEnabled())
        {
            _device.Disable();
        }
        else
        {
            _device.Enable();
        }
    }
    public void VolumeUp()
    {
        int actualVolume = _device.GetVolume();
        int maxVolume = _device.GetMaxVolume();
        if (actualVolume + 1 <= maxVolume)
        {
            _device.SetVolume(actualVolume + 1);
        }
    }
    public void VolumeDown()
    {
        int actualVolume = _device.GetVolume();
        if (actualVolume - 1 >= 0)
        {
            _device.SetVolume(actualVolume - 1);
        }
    }
    public void ChannelUp()
    {
        int actualChannel = _device.GetChannel();
        int maxChannel = _device.GetNumOfChannels();
        _device.SetChannel((actualChannel + 1) % maxChannel);
    }
    public void ChannelDown()
    {
        int actualChannel = _device.GetChannel();
        int maxChannel = _device.GetNumOfChannels();
        _device.SetChannel(((actualChannel - 1) % maxChannel + maxChannel) % maxChannel);
    }
}

class TV : Device
{
    private string name;
    private bool powerOn;
    private int channel;
    private int volume;
    private int maxVolume;
    private int numOfChannels;

    public TV(string inputName)
    {
        name = inputName;
        powerOn = true;
        channel = 0;
        volume = 0;
        maxVolume = 30;
        numOfChannels = 15;
    }

    public bool IsEnabled()
    {
        return powerOn;
    }
    public void Enable()
    {
        powerOn = true;
    }
    public void Disable()
    {
        powerOn = false;
    }
    public void SetVolume(int newVolume)
    {
        volume = newVolume;
    }
    public int GetVolume()
    {
        return volume;
    }
    public int GetMaxVolume()
    {
        return maxVolume;
    }
    public void SetChannel(int newChannel)
    {
        channel = newChannel;
    }
    public int GetChannel()
    {
        return channel;
    }
    public int GetNumOfChannels()
    {
        return numOfChannels;
    }

}

class BasicRemote : Remote
{
    public BasicRemote(Device device) : base(device) { }
}

public class TestBridge
{
    public void TestMe()
    {
        TV televizio = new TV("tevelize");
        BasicRemote remototo = new BasicRemote(televizio);
        remototo.ChannelDown();
        Console.WriteLine(televizio.GetChannel());
    }
}