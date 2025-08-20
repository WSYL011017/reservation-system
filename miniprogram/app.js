App({
  onLaunch() {
    // 配置API基础URL - 完全使用自建后端
    //this.globalData.apiBase = 'http://localhost:5000/api';
    wx.login({
      success: (res) => {
        wx.request({
          url: '/getcode',
        })
      },
    })
    // 获取用户信息
    this.getUserInfo();
  },
  
  globalData: {
    userInfo: null,
    apiBase: 'http://localhost:5000/api'
  },
  
  // 通用请求方法 - 连接自建后端
  request(options) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.apiBase + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          ...options.header
        },
        success: (res) => {
          if (res.data.code === 0) {
            resolve(res.data);
          } else {
            wx.showToast({
              title: res.data.message || '请求失败',
              icon: 'none'
            });
            reject(res.data);
          }
        },
        fail: (err) => {
          wx.showToast({
            title: '网络错误',
            icon: 'none'
          });
          reject(err);
        }
      });
    });
  },
  
  getUserInfo() {
    wx.getUserProfile({
      desc: '用于完善会员资料',
      success: (res) => {
        this.globalData.userInfo = res.userInfo;
        wx.setStorageSync('userInfo', res.userInfo);
      }
    });
  }
});