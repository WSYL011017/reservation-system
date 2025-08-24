// pages/my-reservations/my-reservations.js
const app = getApp();
const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'

Page({
  data: {
    loading: true,
    reservations: [],
    userInfo: {
      avatarUrl: defaultAvatarUrl,
      nickName: ''
    }
  },

  onLoad(options) {
    // 页面加载时获取用户信息
    this.getUserInfoFromStorage();
    this.loadReservations();
  },

  onShow() {
    // 每次显示页面时刷新数据
    this.loadReservations();
  },

  // 从本地存储获取用户信息
  getUserInfoFromStorage() {
    const userInfo = wx.getStorageSync('userInfo') || {};
    this.setData({
      userInfo: {
        avatarUrl: userInfo.avatarUrl || '',
        nickName: userInfo.nickName || ''
      }
    });
  },

  // 获取微信用户信息
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        const userInfo = res.userInfo;
        console.log('获取用户信息成功:', userInfo);
        
        // 保存到本地存储
        wx.setStorageSync('userInfo', {
          avatarUrl: userInfo.avatarUrl,
          nickName: userInfo.nickName
        });
        
        // 更新页面数据
        this.setData({
          userInfo: {
            avatarUrl: userInfo.avatarUrl,
            nickName: userInfo.nickName
          }
        });
        
        wx.showToast({
          title: '获取成功',
          icon: 'success',
          duration: 1500
        });
      },
      fail: (err) => {
        console.log('获取用户信息失败:', err);
        wx.showToast({
          title: '获取失败',
          icon: 'none',
          duration: 2000
        });
      }
    });
  },

  // 加载预约列表
  async loadReservations() {
    try {
      this.setData({ loading: true });
      
      // 这里添加你的预约列表加载逻辑
      // 示例：从本地存储获取预约数据
      const reservations = wx.getStorageSync('reservations') || [];
      
      // 格式化状态文本
      const formattedReservations = reservations.map(item => ({
        ...item,
        statusText: this.getStatusText(item.status),
        createTime: this.formatDate(item.createTime)
      }));
      
      this.setData({
        reservations: formattedReservations,
        loading: false
      });
      
    } catch (error) {
      console.error('加载预约列表失败:', error);
      this.setData({ loading: false });
    }
  },

  // 获取状态文本
  getStatusText(status) {
    const statusMap = {
      'pending': '待确认',
      'confirmed': '已确认',
      'completed': '已完成',
      'cancelled': '已取消'
    };
    return statusMap[status] || status;
  },

  // 格式化日期
  formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  },

  // 跳转到预约页面
  goToReservation() {
    wx.navigateTo({
      url: '/pages/reservation/reservation'
    });
  },

  // 取消预约
  cancelReservation(e) {
    const id = e.currentTarget.dataset.id;
    const index = e.currentTarget.dataset.index;
    
    wx.showModal({
      title: '提示',
      content: '确定要取消这条预约吗？',
      success: (res) => {
        if (res.confirm) {
          // 这里添加取消预约的逻辑
          const reservations = [...this.data.reservations];
          reservations[index].status = 'cancelled';
          reservations[index].statusText = '已取消';
          
          // 更新本地存储
          wx.setStorageSync('reservations', reservations);
          
          this.setData({
            reservations: reservations
          });
          
          wx.showToast({
            title: '取消成功',
            icon: 'success'
          });
        }
      }
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadReservations();
    wx.stopPullDownRefresh();
  }
});