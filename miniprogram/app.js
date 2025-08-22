App({
  onLaunch() {
    // 配置API基础URL - 完全使用自建后端
    // this.globalData.apiBase = 'http://localhost:5000/api';
    wx.login({
      success: (res) => {
        if (res.code) {
          //发起网络请求
          wx.request({
            url: this.globalData.apiBase + '/getcode',
            header: {
              'Content-Type': 'application/json'
            },
            method: 'POST',
            data: {
              code: res.code
            },
            success: res => {
              console.log('res',res.data);
              if (res.data.openid) {
                console.log('成功获取openid:', res.data.openid); // 成功获取到openid
                wx.setStorage(
                  {
                    key: 'token',
                    data: res.data
                  }
                )
              } else {
                console.error('获取openid失败:', res.data.errmsg); // 没有获取到openid，返回错误信息
              }
            },
            fail: err => {
              console.error('请求失败:', err.errMsg); // 请求失败，返回错误信息
            }
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      },
    })
  },

  globalData: {
    userInfo: null,
    apiBase: 'https://cool-correctly-monitor.ngrok-free.app/reservations'
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
  }
});