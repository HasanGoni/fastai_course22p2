# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of super-resolution U-Net architecture
- ResBlock implementation with configurable activation and normalization
- Dynamic model architecture with configurable feature sizes
- Upsampling blocks with skip connections
- Batch normalization support
- Dropout regularization
- Custom activation function support (default: GELU)
- Flexible kernel size configuration (default: 5x5 for initial block)

### Technical Details
- Model Architecture:
  - Configurable feature sizes (32,64,128,256,512,1024)
  - Initial conv block with 5x5 kernel
  - Residual connections in downsampling path
  - Skip connections in upsampling path
  - BatchNorm2d normalization
  - Dropout rate: 0.1
  - GELU activation function

### Dependencies
- PyTorch
- fastai
- numpy
- Jupyter notebooks

### Development
- Implemented in Jupyter notebook format
- Located in `nbs/08_preprocessing.superres_with_unet.ipynb`
- Follows fastai coding style and best practices
- Implements progressive resizing technique for super-resolution
- Uses modern PyTorch practices for model construction

### Documentation
- Jupyter notebooks with detailed explanations
- Code comments following fastai documentation style
- Implementation details and architecture choices explained

[Unreleased]: https://github.com/hasangoni/fastai_course22p2/tree/master