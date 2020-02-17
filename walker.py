from controller import Controller
from actor import Actor
import time
import threading
from datetime import datetime, timedelta

class WalkerThread(threading.Thread):
    def __init__(self, logger, parent, name='WalkerThread'):
        # super(WalkerThread, self).__init__()
        self.parent = parent
        self._stopevent = threading.Event()
        self._isrunning = threading.Event()
        threading.Thread.__init__(self, name=name)
        self.logger = logger
        self.walker = Walker(parent, self.logger, self._stopevent)

    def run(self):
        self._isrunning.set()
        cnt = 0
        self.logger.error('Bot Thread Started!')
        while True:
            cnt = cnt + 1
            cycle = float(self.parent.enCycle.get())

            ed = datetime.now() + timedelta(hours=cycle)
            self.logger.error('[START ' + str(cnt) + 'th Cycle]')
            self.walker.start()
            if self._stopevent.isSet():
                break

            self.logger.warning('On idle time until ' + str(ed))
            while datetime.now() < ed:
                if self._stopevent.isSet():
                    break
                time.sleep(3)
            if self._stopevent.isSet():
                break

        self._stopevent.clear()
        self._isrunning.clear()
        self.logger.error('Bot Thread Ended!')



    def stop(self, timeout=None):
        self._stopevent.set()

    def stopped(self):
        return self._stopevent.is_set()    


class Walker:

    def __init__(self, parent, logger, _stopevent):
        self.parent = parent
        self.logger = logger
        self._stopevent = _stopevent

        self.savedFilename = "followings.dat"
        self.savedFollowers = "followers.dat"

        self.actor = Actor(_stopevent)
        self.controller = self.actor.controller
        self.search_delay = self.actor.get_config('main', 'search_delay')

        self.num_followers = int(self.parent.enFollows.get())
        # self.num_followers = self.actor.get_config('main', 'num_followers')

    def start(self):
        self.followings = []
        self.unfollowings = []

        self.loadNewFollowingList()
        if self._stopevent.isSet():
            return
        self.checkFollowings()
        if self._stopevent.isSet():
            return
        self.removeUnfollowings()
        if self._stopevent.isSet():
            return
        self.startNewFollowings()
        if self._stopevent.isSet():
            return
        self.saveFollowingList()
        if self._stopevent.isSet():
            return

        # self.logger.info('-> Check Following')
        # self.controller.mouse_click_name('profile')
        # self.controller.mouse_click_name('followers')
        # time.sleep(4)
        # self.controller.mouse_click_name('search')
        # self.controller.key_input('following')
        

    def loadNewFollowingList(self):
        self.logger.info('-> Loading Data')
        try:
            self.f = open(self.savedFilename, "r")
            for x in self.f:
                self.followings.append(x[:-1])
        finally:
            self.f.close()
        self.logger.info('<- Loading Data')

    def checkFollowings(self):
        self.logger.info('-> Check Following')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('followers')
        time.sleep(4)

        new_followings = []
        self.unfollowings = []

        self.file_object = open(self.savedFollowers, 'a')
            # Append 'hello' at the end of file

        for following in self.followings:
            if self._stopevent.isSet():
                break
            self.controller.mouse_click_name('search')
            self.controller.key_input(following)
            time.sleep(self.search_delay)

            res = self.actor.capture_search_result()
            if res == True: # Keep
                new_followings.append(following)
                self.file_object.write("hello")
                self.logger.critical('    ' + 'O ' + following)
            else : # remove
                self.unfollowings.append(following)
                self.logger.critical('    ' + 'X ' + following)

            self.controller.mouse_click_name('search')
            self.controller.key_remove(following)

        self.file_object.close()
        # self.followings = new_followings
        self.followings = []
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Check Following')

    def test(self):
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')
        self.controller.mouse_click_name('discover_suggested')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('followers')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('following')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('search')
        self.controller.mouse_click_name('discover_plus')

    def removeUnfollowings(self):
        self.logger.info('-> Remove Followings')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('following')
        time.sleep(4)

        for unfollowing in self.unfollowings:
            if self._stopevent.isSet():
                break
            self.controller.mouse_click_name('search')
            self.controller.key_input(unfollowing)
            time.sleep(self.search_delay)

            res = self.actor.capture_search_result()
            if res == True: # Keep
                self.actor.unfollow_one(unfollowing)
                self.logger.critical('    ' + '- ' + unfollowing)

            else :
                self.followings.append(unfollowing)
                self.logger.critical('    ' + '! ' + unfollowing)

            self.controller.mouse_click_name('search')
            self.controller.key_remove(unfollowing)

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Remove Followings')

    def startNewFollowings(self):
        self.logger.info('-> Start Followings')

        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('profile_menu')
        self.controller.mouse_click_name('discover')

        # self.controller.mouse_click_name('discover_suggested')
        self.controller.item_scroll_prepare()


        for i in range(self.num_followers):
            if self._stopevent.isSet():
                break
            self.controller.item_scroll_down()
            name = self.actor.follow_one()
            if name != '':
                self.followings.append(name)
                self.logger.critical('    ' + '+ ' + name)

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Start Followings')

    def saveFollowingList(self):
        self.logger.info('-> Save Data')
        with open(self.savedFilename, 'w+') as f:
            for name in self.followings:
                f.write(name + '\n')
        self.logger.info('<- Save Data')
