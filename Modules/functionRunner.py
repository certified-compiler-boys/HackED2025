import ImagePostProcessing as IMP
import matplotlib.pyplot as plt
from skimage import io

pathTest = 'Parrot.jpg'
original = io.imread(pathTest)
output_image = IMP.color_quantize(original)

plt.imshow(output_image)
plt.axis('off')
plt.show()

