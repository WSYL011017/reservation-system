const app = getApp()

Page({
  data: {
    showLoginModal: false
  },
  onLoad() {
    // 从本地缓存中获取真实用户信息
    const realUserInfo = wx.getStorageSync('realUserInfo');
    if (!realUserInfo || !realUserInfo.avatarUrl || !realUserInfo.nickName) {
      this.setData({
        showLoginModal: true,
        userInfo: null
      });
      wx.showModal({
        title: '提示',
        content: '未登录，请先登录！',
        showCancel: false,
        success: res => {
          if (res.confirm) {
            console.log('用户点击确定')
            this.setData({
              showLoginModal: true
            })
            wx.navigateTo({
              url: '/pages/login/login',
            })
          }
        }
      })
    } else {
      // 如果有用户信息，更新数据
      this.setData({
        showLoginModal: false,
        userInfo: realUserInfo
      });
    }
  },
  tologin() {

  },

  goToReservation() {
    const realUserInfo = wx.getStorageSync('realUserInfo');
    if (!realUserInfo || !realUserInfo.avatarUrl || !realUserInfo.nickName) {
      this.setData({
        showLoginModal: true,
        userInfo: null
      });
      wx.showModal({
        title: '提示',
        content: '未登录，请先登录！',
        showCancel: false,
        success: res => {
          if (res.confirm) {
            console.log('用户点击确定')
            this.setData({
              showLoginModal: true
            })
            wx.navigateTo({
              url: '/pages/login/login',
            })
          }
        }
      })
    } else {
      wx.navigateTo({
        url: '/pages/reservation/reservation'
      });
    }
  }
});