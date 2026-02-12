"""
MapleDiseaseValueHolder - 从Java源文件转换而来
对应Java源文件: client/MapleDiseaseValueHolder.java
包路径: client
"""


class MapleDiseaseValueHolder:
    """
    类 MapleDiseaseValueHolder - 从Java类转换
    实现接口: Serializable
    """

    # 静态字段 (Static fields)
    serialVersionUID = 9179541993413738569

    def __init__(self, disease: Any, startTime: int, length: int):
        """初始化 MapleDiseaseValueHolder"""
        self.startTime = 0
        self.length = 0
        self.disease = None


