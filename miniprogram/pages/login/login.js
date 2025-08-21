// pages/login/login.js
const app = getApp();

Page({
  data: {
    canIUseGetUserProfile: false,
    isLoggingIn: false,
    hasAgreed: false,
    showAgreementModal: false,
    modalTitle: '',
    modalContent: '',
    
    // 用户协议内容
    userAgreementContent: `
      <h3>用户协议</h3>
      <p><strong>生效日期：</strong>2024年1月1日</p>
      
      <h4>1. 重要须知</h4>
      <p>1.1 本协议是您与本小程序运营方之间关于使用本小程序服务所订立的协议。</p>
      <p>1.2 请您仔细阅读本协议，您点击"同意"或实际使用本服务即表示您已充分阅读、理解并同意本协议的全部内容。</p>
      
      <h4>2. 服务内容</h4>
      <p>2.1 本小程序提供在线预约服务，包括但不限于服务预约、预约管理等功能。</p>
      <p>2.2 我们有权根据业务发展需要调整服务内容。</p>
      
      <h4>3. 用户权利与义务</h4>
      <p>3.1 您有权按照本协议约定使用本服务。</p>
      <p>3.2 您应保证提供的个人信息真实、准确、完整。</p>
      <p>3.3 您不得利用本服务从事违法违规活动。</p>
      
      <h4>4. 隐私保护</h4>
      <p>4.1 我们高度重视用户隐私，严格按照《隐私政策》保护您的个人信息。</p>
      <p>4.2 未经您的同意，我们不会向第三方披露您的个人信息。</p>
      
      <h4>5. 协议变更</h4>
      <p>5.1 我们有权根据业务发展需要修改本协议。</p>
      <p>5.2 修改后的协议将在本页面公布，公布后即生效。</p>
    `,
    
    // 隐私政策内容
    privacyPolicyContent: `
      <h3>隐私政策</h3>
      <p><strong>生效日期：</strong>2024年1月1日</p>
      
      <h4>1. 信息收集</h4>
      <p>1.1 为提供服务，我们需要收集以下信息：</p>
      <ul>
        <li>微信昵称、头像、性别</li>
        <li>微信OpenID、UnionID</li>
        <li>预约相关信息</li>
        <li>设备信息、日志信息</li>
      </ul>
      
      <h4>2. 信息使用</h4>
      <p>2.1 我们收集的信息将用于：</p>
      <ul>
        <li>提供预约服务</li>
        <li>用户身份识别</li>
        <li>服务优化与改进</li>
        <li>安全保障与风险防范</li>
      </ul>
      
      <h4>3. 信息共享</h4>
      <p>3.1 我们不会与第三方共享您的个人信息，但以下情况除外：</p>
      <ul>
        <li>获得您的明确同意</li>
        <li>法律法规要求</li>
        <li>维护社会公共利益</li>
      </ul>
      
      <h4>4. 信息保护</h4>
      <p>4.1 我们采用业界标准的安全措施保护您的信息。</p>
      <p>4.2 我们会定期审查信息收集、存储和处理方面的做法。</p>
      
      <h4>5. 您的权利</h4>
      <p>5.1 您有权访问、修改、删除您的个人信息。</p>
      <p>5.2 您可以通过小程序设置撤回授权。</p>
      
      <h4>6. 联系我们</h4>
      <p>如有任何疑问，请联系我们：support@example.com</p>
    `
  },

  onLoad() {
    // 检查是否支持getUserProfile
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
    
    // 检查是否已同意协议
    const hasAgreed = wx.getStorageSync('hasAgreedAgreement') || false;
    this.setData({
      hasAgreed: hasAgreed
    });
  },

  // 处理协议勾选
  handleAgreementChange(e) {
    const hasAgreed = e.detail.value.includes('agreed');
    this.setData({
      hasAgreed: hasAgreed
    });
    wx.setStorageSync('hasAgreedAgreement', hasAgreed);
  },

  // 显示用户协议
  showUserAgreement() {
    this.setData({
      showAgreementModal: true,
      modalTitle: '用户协议',
      modalContent: this.data.userAgreementContent
    });
  },

  // 显示隐私政策
  showPrivacyPolicy() {
    this.setData({
      showAgreementModal: true,
      modalTitle: '隐私政策',
      modalContent: this.data.privacyPolicyContent
    });
  },

  // 隐藏弹窗
  hideModal() {
    this.setData({
      showAgreementModal: false
    });
  },

  // 阻止冒泡
  preventBubble() {
    // 空函数，用于阻止事件冒泡
  },

  // 处理登录
  handleLogin() {
    if (!this.data.hasAgreed) {
      wx.showToast({
        title: '请先阅读并同意用户协议和隐私政策',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    if (this.data.isLoggingIn) return;

    this.setData({
      isLoggingIn: true
    });

    if (this.data.canIUseGetUserProfile) {
      // 使用getUserProfile获取用户信息
      wx.getUserProfile({
        desc: '用于完善用户资料',
        success: (res) => {
          this.handleLoginSuccess(res.userInfo);
        },
        fail: (err) => {
          console.log('用户拒绝授权：', err);
          wx.showToast({
            title: '需要授权才能使用完整功能',
            icon: 'none',
            duration: 2000
          });
          this.setData({
            isLoggingIn: false
          });
        }
      });
    } else {
      // 兼容旧版本
      wx.getUserInfo({
        success: (res) => {
          this.handleLoginSuccess(res.userInfo);
        },
        fail: (err) => {
          console.log('用户拒绝授权：', err);
          wx.showToast({
            title: '需要授权才能使用完整功能',
            icon: 'none',
            duration: 2000
          });
          this.setData({
            isLoggingIn: false
          });
        }
      });
    }
  },

  // 处理登录成功
  handleLoginSuccess(userInfo) {
    // 保存用户信息到全局和本地存储
    app.globalData.userInfo = userInfo;
    wx.setStorageSync('userInfo', userInfo);

    // 获取code并发送到后端
    wx.login({
      success: (loginRes) => {
        if (loginRes.code) {
          wx.request({
            url: app.globalData.apiBase + '/login',
            method: 'POST',
            data: {
              code: loginRes.code,
              userInfo: userInfo
            },
            success: (res) => {
              if (res.data.openid) {
                // 保存登录态
                wx.setStorageSync('token', res.data);
                
                wx.showToast({
                  title: '登录成功',
                  icon: 'success',
                  duration: 1000
                });

                // 延迟跳转
                setTimeout(() => {
                  const pages = getCurrentPages();
                  if (pages.length > 1) {
                    wx.navigateBack({
                      delta: 1
                    });
                  } else {
                    wx.switchTab({
                      url: '/pages/index/index'
                    });
                  }
                }, 1000);
              }
            },
            fail: () => {
              wx.showToast({
                title: '网络错误，请重试',
                icon: 'none'
              });
            },
            complete: () => {
              this.setData({
                isLoggingIn: false
              });
            }
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '获取登录凭证失败',
          icon: 'none'
        });
        this.setData({
          isLoggingIn: false
        });
      }
    });
  }
});