from PIL import Image
import os

def replace_black_with_blue(input_path, output_path, target_color_hex="#1989fa"):
    """
    将PNG图片中的黑色替换为指定的蓝色
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param target_color_hex: 目标蓝色十六进制值
    """
    # 将十六进制颜色转换为RGB
    target_color_hex = target_color_hex.lstrip('#')
    target_rgb = tuple(int(target_color_hex[i:i+2], 16) for i in (0, 2, 4))
    
    # 打开图片
    img = Image.open(input_path).convert('RGBA')
    pixels = img.load()
    
    # 获取图片尺寸
    width, height = img.size
    
    # 创建新图片
    new_img = Image.new('RGBA', (width, height))
    new_pixels = new_img.load()
    
    # 遍历每个像素
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # 如果像素不是完全透明
            if a > 0:
                # 判断是否为黑色或接近黑色（图标颜色）
                if r < 50 and g < 50 and b < 50:  # 接近黑色的范围
                    # 替换为目标蓝色，保持透明度
                    new_pixels[x, y] = target_rgb + (a,)
                else:
                    # 保持其他颜色不变
                    new_pixels[x, y] = (r, g, b, a)
            else:
                # 保持透明像素不变
                new_pixels[x, y] = (r, g, b, a)
    
    # 保存新图片
    new_img.save(output_path)
    print(f"✅ 颜色替换完成: {output_path}")

if __name__ == "__main__":
    # 项目路径配置
    project_path = "c:/Users/suyal/Desktop/Reservation system"
    images_path = os.path.join(project_path, "images")
    
    # 定义文件路径
    order_active_path = os.path.join(images_path, "order-active.png")
    home_active_path = os.path.join(images_path, "home-active.png")
    output_path = os.path.join(images_path, "order-active_blue.png")
    
    # 使用项目主题蓝色 #1989fa（与home-active保持一致）
    theme_blue = "#1989fa"
    
    print("🎨 开始为order-active.png更换颜色...")
    print(f"📁 原文件: {order_active_path}")
    print(f"🎯 目标蓝色: {theme_blue}")
    
    try:
        # 执行颜色替换
        replace_black_with_blue(order_active_path, output_path, theme_blue)
        
        # 备份原文件
        backup_path = os.path.join(images_path, "order-active_original.png")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(order_active_path, backup_path)
        
        # 替换为新文件
        os.rename(output_path, order_active_path)
        
        print("🎉 颜色更换完成！")
        print(f"💾 原文件已备份: {backup_path}")
        
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        print("💡 请确保已安装Pillow库: pip install pillow")