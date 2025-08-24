const app = getApp()

Page({
  data: {},
  onLoad() {
    
  },

  goToReservation() {
    const phoneNumber = wx.getStorageSync('phoneNumber');
    if (!phoneNumber) {
      app.tologin()
    } else {
      wx.navigateTo({
        url: '/pages/reservation/reservation'
      });
    }
  }
});