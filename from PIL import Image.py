from PIL import Image
import os

def fill_png_with_color(input_path, output_path, color_hex):
    """
    为PNG图片填充指定颜色
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param color_hex: 十六进制颜色值，如"#1989fa"
    """
    # 将十六进制颜色转换为RGB
    color_hex = color_hex.lstrip('#')
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    
    # 打开原始图片
    img = Image.open(input_path)
    
    # 创建一个新的图片，填充指定颜色
    new_img = Image.new('RGBA', img.size, color_rgb + (255,))
    
    # 如果原图有透明通道，保留透明度
    if img.mode == 'RGBA':
        # 将原图粘贴到新图上，使用原图作为遮罩
        new_img.paste(img, (0, 0), img)
    else:
        # 如果没有透明通道，直接覆盖
        new_img.paste(img, (0, 0))
    
    # 保存新图片
    new_img.save(output_path)
    print(f"图片已保存到: {output_path}")

# 使用示例
if __name__ == "__main__":
    # 项目路径
    project_path = "c:/Users/suyal/Desktop/Reservation system"
    images_path = os.path.join(project_path, "images")
    
    # 文件路径
    empty_path = os.path.join(images_path, "order.png")
    output_path = os.path.join(images_path, "order_blue.png")
    
    # 项目主题色
    theme_color = "#1989fa"
    
    # 执行颜色填充
    fill_png_with_color(empty_path, output_path, theme_color)
    
    # 备份原文件并替换
    backup_path = os.path.join(images_path, "order_backup.png")
    os.rename(empty_path, backup_path)
    os.rename(output_path, empty_path)
    
    print("颜色填充完成！")