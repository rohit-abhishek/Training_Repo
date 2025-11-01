class TV: 
    def __init__(self) -> None:
        self.isOn = False 
        self.isMuted = False 
        self.channelList = [2,4,5,7,9,11,20,36,44,54,65]
        self.nChannels = len(self.channelList)
        self.channelIndex = 0 
        self.VOLUME_MIN = 0 
        self.VOLUME_MAX = 10 
        self.volume = self.VOLUME_MAX // 2

    def power(self):
        self.isOn = not self.isOn

    def volumeUp(self):

        if not self.isOn: 
            return 
        if self.isMuted:
            self.isMuted = False 
        if self.volume < self.VOLUME_MAX:
            self.volume += 1

    def volumeDown(self):

        if not self.isOn: 
            return 
        if self.isMuted:
            self.isMuted = False 
        if self.volume > self.VOLUME_MIN:
            self.volume -= 1

    def channelUp(self):

        if not self.isOn: 
            return 
        self.channelIndex += 1

        if self.channelIndex > self.nChannels:
            self.channelIndex = 0

    def channelDown(self):

        if not self.isOn: 
            return 
        self.channelIndex -= 1

        if self.channelIndex < 0:
            self.channelIndex = self.nChannels - 1


    def mute(self):
        if not self.isOn: 
            return 

        self.isMuted = not self.isMuted

    def setChannel(self, newChannel):
        if newChannel in self.channelList:
            self.channelIndex = self.channelList.index(newChannel)

    def show(self):

        print ()
        print ('TV Status ')

        if self.isOn:
            print ('TV is : On')
            print ('channel is: ', self.channelList[self.channelIndex])

            if self.isMuted:
                print ('Volume is ', self.volume, '(sound is muted)')
            else: 
                print ('Volume is ', self.volume)
        else: 
            print ('TV is : Off')

otv = TV()
otv.show()

otv.power()
otv.mute()
otv.show()

otv.setChannel(11)
otv.volumeUp()
otv.show()
