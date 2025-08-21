const app = getApp();

Page({
  data: {
    reservations: [],
    loading: true,
    phone: ''
  },
  
  onLoad() {
    this.getUserPhone();
  },
  
  onShow() {
    if (this.data.phone) {
      this.loadReservations();
    }
  },
  
  getUserPhone() {
    // 从本地存储获取手机号
    const phone = wx.getStorageSync('userPhone') || '';
    this.setData({ phone });
  },
  
  // 加载用户预约数据
  async loadReservations() {
    if (!this.data.phone) {
      this.setData({ loading: false });
      return;
    }
    
    this.setData({ loading: true });
    
    try {
      const res = await app.request({ 
        url: '/reservations',
        data: { phone: this.data.phone }
      });
      
      const reservations = res.data.map(item => ({
        ...item,
        statusText: this.getStatusText(item.status),
        date: item.service_date,
        time: item.service_time,
        name: item.customer_name,
        phone: item.customer_phone
      }));
      
      this.setData({
        reservations,
        loading: false
      });
      
      wx.stopPullDownRefresh();
    } catch (error) {
      console.error('获取预约数据失败:', error);
      this.setData({ loading: false });
      wx.showToast({
        title: '获取数据失败',
        icon: 'none'
      });
    }
  },
  
  // 状态文本转换
  getStatusText(status) {
    const statusMap = {
      'pending': '待确认',
      'confirmed': '已确认',
      'completed': '已完成',
      'cancelled': '已取消'
    };
    return statusMap[status] || status;
  },
  
  // 取消预约
  async cancelReservation(e) {
    const { id } = e.currentTarget.dataset;
    
    wx.showModal({
      title: '确认取消',
      content: '确定要取消这个预约吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await app.request({
              url: `/reservations/${id}/cancel`,
              method: 'PUT',
              data: { phone: this.data.phone }
            });
            
            wx.showToast({ title: '取消成功' });
            this.loadReservations();
          } catch (error) {
            wx.showToast({ title: '取消失败', icon: 'none' });
          }
        }
      }
    });
  },
  
  // 下拉刷新
  onPullDownRefresh() {
    this.loadReservations();
  },
  
  // 跳转到预约页面
  goToReservation() {
    wx.navigateTo({ url: '/pages/reservation/reservation' });
  }
});