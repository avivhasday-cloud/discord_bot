



class MessageFormater:

    def __init__(self):
        self.italic_style = '*'
        self.bold_italic_style = "***"
        self.code_block_style = "```"
        self.block_quote_style = ">"


    def get_italian_format(self,message:str) -> str:
        return f"{self.italic_style} {message} {self.italic_style}"

    def get_italian_code_block_format(self, message:str) -> str:
        lines = message.split("\n")
        header = f"{self.bold_italic_style} {lines[0]} {self.bold_italic_style}"
        formated_str = f'{self.code_block_style}'
        formated_str += header
        index = 1 if len(lines) > 1 else 0

        for line in lines[index::]:
            formated_str += f"{self.italic_style} {line} {self.italic_style} \n"

        formated_str  += self.code_block_style
        return formated_str

    def get_block_quote_format(self, message:str) -> str:
        return f"{self.block_quote_style} {message}"