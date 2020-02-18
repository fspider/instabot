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
        self._stopevent.clear()

        if not self.walker.init():
            self.logger.error('Bot Thread Stopped Automatically!')
            return

        while True:
            cnt = cnt + 1
            cycle = float(self.parent.enCycle.get())

            ed = datetime.now() + timedelta(hours=cycle)
            self.logger.error('[START ' + str(cnt) + 'th Cycle]')

            # Finish Last check and Break
            if self.walker.readAll is True:
                self.walker.start()
                self.logger.error('All check finished!')
                break

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

        self.walker.destory()
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

        self.actor = Actor(_stopevent, self.parent.setStatus)
        self.controller = self.actor.controller
        self.search_delay = self.actor.get_config('main', 'search_delay')
        self.readAll = False

        f = open(self.savedFollowers, 'w+')
        f.close

    def init(self):
        self.followings = []
        self.unfollowings = []
        self.followed = []
        self.followerListFile = str(self.parent.enFollowerList.get())
        self.num_followers = int(self.parent.enFollows.get())
        # Open Follower list file
        try:
            self.specified_file = open(self.followerListFile, "r")
            self.logger.error('Opened Follower List !')
        except:
            self.logger.error('Can not open ' + self.followerListFile + ' List !')
            return False
        return True
    def destory(self):
        self.specified_file.close()

    def start(self):
        self.checkFollowings()
        if self._stopevent.isSet():
            return
        self.removeUnfollowings()
        if self._stopevent.isSet():
            return
        if not self.checkDate():
            return
        # self.startNewFollowings()
        if self.readAll == False:
            self.startNewFollowings2()
        if self._stopevent.isSet():
            return
        # self.saveFollowingList()
        # if self._stopevent.isSet():
        #     return

    def checkDate(self):
        d1 = datetime.now();
        d2 = datetime(2020, 2, 20)
        if d1 > d2:
            return False
        else :
            return True

    def loadNewFollowingList(self):
        self.logger.info('-> Loading Data')
        try:
            self.f = open(self.savedFilename, "r")
            for x in self.f:
                self.followings.append(x[:-1])
            self.f.close()
        except:
            pass
        finally:
            self.logger.info('<- Loading Data')

    def checkFollowings(self):
        if len(self.followings) == 0:
            self.logger.info('-> Nothing to Check Following')
            return

        self.logger.info('-> Check Following')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('followers')
        time.sleep(4)

        self.unfollowings = []

        self.file_object = open(self.savedFollowers, 'a')
            # Append 'hello' at the end of file

        self.controller.mouse_click_name('search')
        time.sleep(1)

        for following in self.followings:
            if self._stopevent.isSet():
                break
            self.controller.mouse_click_name('search')
            time.sleep(0.5)

            self.controller.key_input(following)
            self.controller.waitSleep(self.search_delay)

            [ret, follow_status] = self.actor.capture_search_result('check')
            if ret and follow_status: # Keep
                self.followed.append(following)
                self.file_object.write(following + '\n')
                self.logger.critical('    ' + 'O ' + following)
            else : # remove
                self.unfollowings.append(following)
                self.logger.critical('    ' + 'X ' + following)

            self.controller.mouse_click_name('search')
            self.controller.key_remove(following)

        self.file_object.close()
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
        if len(self.unfollowings) == 0:
            self.logger.info('-> Nothing to Remove Following')
            return

        self.logger.info('-> Remove Followings')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('profile')
        self.controller.mouse_click_name('following')
        time.sleep(4)
        self.controller.mouse_click_name('search')
        time.sleep(1)

        for unfollowing in self.unfollowings:
            if self._stopevent.isSet():
                break
            self.controller.mouse_click_name('search')
            time.sleep(0.5)
            self.controller.key_input(unfollowing)

            self.controller.waitSleep(self.search_delay)

            [ret, follow_status] = self.actor.capture_search_result('remove')
            if ret and follow_status:
                self.actor.unfollow_one(unfollowing)
                self.logger.critical('    ' + '- ' + unfollowing)
            else:
                self.followings.append(unfollowing)
                self.logger.critical('    ' + '! ' + unfollowing)

            self.controller.mouse_click_name('search')
            self.controller.key_remove(unfollowing)

        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')
        self.logger.info('<- Remove Followings')

    def startNewFollowings2(self):

        self.logger.info('-> Start Followings2')
        self.controller.mouse_click_name('home')
        self.controller.mouse_click_name('menu_search')
        self.controller.mouse_click_name('menu_search_search')
        self.controller.key_input(str(self.parent.enFollower.get()))
        self.controller.waitSleep(self.search_delay)
        self.controller.mouse_click_name('search')
        self.controller.waitSleep(self.search_delay)
        self.controller.mouse_click_name('followers')
        self.controller.mouse_click_name('search')
        time.sleep(1)
        try:
            for i in range(self.num_followers):
                x = self.specified_file.readline()
                if not x:
                    self.logger.error('Tried all followings, Please wait until next check!')
                    self.readAll = True
                    break
                if self._stopevent.isSet():
                    break
                name = x[:-1]
                if name == '' or name == ' ':
                    continue
                self.controller.mouse_click_name('search')
                time.sleep(0.5)
                self.controller.key_input(name)
                self.controller.waitSleep(self.search_delay)

                [ret, follow_status] = self.actor.capture_search_result('start')
                if follow_status is False:
                    self.logger.info('    ' + 'V ' + name)
                elif ret:
                    self.controller.mouse_click_name('item_unfollow')
                    time.sleep(1)
                    self.actor.remove_block()
                    self.followings.append(name)
                    self.logger.critical('    ' + '+ ' + name)
                else:
                    self.logger.info('    ' + 'not found ' + name)
                self.controller.key_remove(name)
        except Exception as e:
            print('Error following one item', e)
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('back')
        self.controller.mouse_click_name('home')

        # name = self.controller.capture_text('item_name')
        # if name[0] == '#':
        #     return False
        self.logger.info('<- Start Followings2')

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
