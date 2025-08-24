// miniprogram/app.js
App({
  async onLaunch() {
    const updateManager = wx.getUpdateManager()
    updateManager.onUpdateReady(() => {
      wx.showModal({
        title: '更新提示',
        content: '新版本已经准备好，是否重启应用？',
        complete: (res) => {
          if (res.confirm) {
            updateManager.applyUpdate()
          }
        }
      })
    })
    // 程序加载时自动获取token
    try {
      console.log('程序启动，开始获取token...');
      await this.ensureToken();
      console.log('token获取成功');
    } catch (error) {
      console.error('程序启动时获取token失败:', error);
      // 不显示错误给用户，后续操作会再次尝试获取
    }
  },

  globalData: {
    userInfo: null,
    apiBase: 'https://cool-correctly-monitor.ngrok-free.app/reservations'
  },

  // 通用请求方法
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
          resolve(res.data);
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

  // 修改 getcode - 确保 Promise 正确执行
  async getcode() {
    return new Promise((resolve, reject) => {
      wx.login({
        success: async (res) => {
          if (res.code) {
            try {
              const response = await this.request({
                url: '/getcode',
                method: 'POST',
                data: { code: res.code }
              });
              
              console.log('getcode response:', response);
              
              if (response && response.access_token) {
                wx.setStorageSync('token', response);
                resolve(response);
              } else {
                reject(new Error('获取token失败'));
              }
            } catch (error) {
              console.error('getcode error:', error);
              reject(error);
            }
          } else {
            reject(new Error('wx.login 失败'));
          }
        },
        fail: reject
      });
    });
  },

  // 添加获取token的便捷方法
  async ensureToken() {
    let token = wx.getStorageSync('token');
    
    // 检查token是否有效（这里简化处理，实际应该有有效期检查）
    if (!token || !token.access_token) {
      console.log('需要重新获取token...');
      token = await this.getcode();
    }
    
    return token;
  },

  tologin() {
    wx.showModal({
      title: '提示',
      content: '未登录，请先登录！',
      showCancel: false,
      success: res => {
        if (res.confirm) {
          wx.navigateTo({
            url: '/pages/login/login',
          });
        }
      }
    });
  },
});