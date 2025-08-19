from PIL import Image
import os

def tint_image_with_theme_color(input_path, output_path, theme_color_hex="#1989fa"):
    """
    将PNG图片调整为指定的主题色
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径  
    :param theme_color_hex: 主题色十六进制值
    """
    # 将十六进制颜色转换为RGB
    theme_color_hex = theme_color_hex.lstrip('#')
    theme_rgb = tuple(int(theme_color_hex[i:i+2], 16) for i in (0, 2, 4))
    
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
                # 计算灰度值（用于确定亮度）
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # 根据灰度值调整主题色的亮度
                factor = gray / 255.0
                
                # 应用主题色，保持透明度
                new_r = int(theme_rgb[0] * factor)
                new_g = int(theme_rgb[1] * factor)
                new_b = int(theme_rgb[2] * factor)
                
                new_pixels[x, y] = (new_r, new_g, new_b, a)
            else:
                # 保持透明像素不变
                new_pixels[x, y] = (r, g, b, a)
    
    # 保存新图片
    new_img.save(output_path)
    print(f"✅ 图片颜色已更新: {output_path}")

if __name__ == "__main__":
    # 项目路径配置
    project_path = "c:/Users/suyal/Desktop/Reservation system"
    images_path = os.path.join(project_path, "images")
    
    # 定义文件路径
    first_image = os.path.join(images_path, "home-active.png")  # 第一个图片（参考）

    second_image = os.path.join(images_path, "order-active.png")   # 第二个图片（需要修改）
    
    # 输出路径
    output_path = os.path.join(images_path, "order_colored.png")
    
    # 使用项目主题色 #1989fa
    theme_color = "#1989fa"
    
    print("🎨 开始为第二个图片填充颜色...")
    print(f"📁 输入图片: {second_image}")
    print(f"🎯 主题色: {theme_color}")
    
    try:
        # 执行颜色填充
        tint_image_with_theme_color(second_image, output_path, theme_color)
        
        # 备份原文件
        backup_path = os.path.join(images_path, "empty_original.png")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(second_image, backup_path)
        
        # 替换为新文件
        os.rename(output_path, second_image)
        
        print("🎉 颜色填充完成！")
        print(f"💾 原文件已备份: {backup_path}")
        
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")