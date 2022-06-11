require "chunky_png"

def to_framebuf(img, sx, sy, w, h)
  buf_size = w * (h / 8.0).ceil
  buf = Array.new(buf_size, 0)
  str = []
  h.times do |dy|
    w.times do |dx|
      x = sx + dx
      y = sy + dy
      col = (img[x, y] == ChunkyPNG::Color::BLACK)
      str << (col ? "@" : " ")
      idx = (dy / 8) * w + dx
      if col
        buf[idx] |= (1 << (dy % 8))
      end
    end
    str << "\n"
  end
  #print str.join
  p buf.each_slice(w).to_a
  [w, h] + buf
end

img = ChunkyPNG::Image.from_file("font.png")

bin = to_framebuf(img, 0, 0, 32, 48)

11.times do |n|
  bin = to_framebuf(img, n * 32 + 4, 0, 32 - 8, 48)
  IO.binwrite("font_#{n}.bin", bin.pack("C*"))
end
