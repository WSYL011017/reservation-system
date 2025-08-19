const app = getApp();

Page({
  data: {
    date: '',
    time: '',
    today: '',
    maxDate: '',
    loading: false,
    formData: {
      name: '',
      phone: '',
      remark: ''
    },
    services: [],
    timeSlots: []
  },
  
  onLoad() {
    // 设置日期范围
    const today = new Date();
    const maxDate = new Date();
    maxDate.setDate(today.getDate() + 30);
    
    this.setData({
      today: this.formatDate(today),
      maxDate: this.formatDate(maxDate)
    });
    
    // 加载服务类型
    this.loadServices();
  },
  
  formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  },
  
  // 加载服务类型
  async loadServices() {
    try {
      const res = await app.request({ url: '/services' });
      this.setData({ services: res.data });
    } catch (error) {
      console.error('加载服务失败:', error);
    }
  },
  
  // 加载时间槽
  async loadTimeSlots() {
    if (!this.data.date) return;
    
    try {
      const res = await app.request({ 
        url: '/time-slots',
        data: { date: this.data.date }
      });
      this.setData({ timeSlots: res.data });
    } catch (error) {
      console.error('加载时间槽失败:', error);
    }
  },
  
  onInputChange(e) {
    const { field } = e.currentTarget.dataset;
    const { value } = e.detail;
    
    this.setData({
      [`formData.${field}`]: value
    });
  },
  
  bindDateChange(e) {
    this.setData({ 
      date: e.detail.value 
    }, () => {
      this.loadTimeSlots();
    });
  },
  
  bindTimeChange(e) {
    this.setData({ time: e.detail.value });
  },
  
  async formSubmit(e) {
    const formData = this.data.formData;
    
    // 验证必填项
    if (!formData.name || !formData.phone || !this.data.date || !this.data.time) {
      wx.showToast({ title: '请填写完整信息', icon: 'none' });
      return;
    }
    
    // 验证手机号
    if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      wx.showToast({ title: '手机号格式不正确', icon: 'none' });
      return;
    }
    
    this.setData({ loading: true });
    
    try {
      const res = await app.request({
        url: '/reservations',
        method: 'POST',
        data: {
          ...formData,
          service_type: '标准预约', // 默认服务类型
          service_date: this.data.date,
          service_time: this.data.time
        }
      });
      
      wx.navigateTo({
        url: `/pages/success/success`
      });
      
    } catch (error) {
      console.error('预约失败:', error);
    } finally {
      this.setData({ loading: false });
    }
  }
});