import ImagePostProcessing as IMP
import matplotlib.pyplot as plt

pathTest = 'Parrot.jpg'
output_image = IMP.color_quantize(pathTest)

plt.imshow(output_image)
plt.axis('off')
plt.show()

