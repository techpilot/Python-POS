from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.modalview import ModalView

import re
from pymongo import MongoClient

Builder.load_file('till_operator/operator.kv')


class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        self.db = client.silverpos
        self.stocks = self.db.stocks

        self.cart = []
        self.qty = []
        self.total = 0.00  # self.ids.qty_inp.text

    def logout(self):
        self.parent.parent.current = 'scrn_si'

    def update_purchases(self):
        pcode = self.ids.code_inp.text
        products_container = self.ids.products

        target_code = self.stocks.find_one({'product_code': pcode})
        if target_code == None:
            pass
        else:
            details = BoxLayout(size_hint_y=None, height=30,
                                pos_hint={'top': 1})
            products_container.add_widget(details)

            code = Label(text=pcode, size_hint_x=.3,
                         bold=True, color=(.06, .45, .45, 1))
            name = Label(text=target_code['product_name'],
                         size_hint_x=.3, color=(.06, .45, .45, 1))
            qty = Label(text=str(self.ids.qty_inp.text),
                        size_hint_x=.1, color=(.06, .45, .45, 1))
            disc = Label(text=str(self.ids.disc_inp.text),
                         size_hint_x=.1, color=(.06, .45, .45, 1))
            price = Label(
                text=str(target_code['product_price']), size_hint_x=.1, color=(.06, .45, .45, 1))

            total = Label(text=str(float(price.text) * int(self.ids.qty_inp.text) - int(self.ids.disc_inp.text)), size_hint_x=.2,
                          color=(.06, .45, .45, 1))
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(disc)
            details.add_widget(price)
            details.add_widget(total)

            # Update Preview
            pname = name.text
            pprice = float(price.text) * int(self.ids.qty_inp.text)
            pqty = str(self.ids.qty_inp.text)  # 1

            # Discount implementation
            try:
                disc_var = self.ids.disc_inp.text
                if disc_var == None:
                    pass  # disc_var = 0
                else:
                    discount = int(self.ids.disc_inp.text)
                    if discount > 0:
                        pprice -= discount
                    else:
                        pprice
            except ValueError:
                print("something just went wrong")

            self.total += pprice

            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t\t\t\t' + \
                str(self.total)
            self.ids.cur_product.text = pname
            self.ids.cur_price.text = str(pprice)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]

            # ptarget = -1
            # for i, c in enumerate(self.cart):
            #     if c == pcode:
            #         ptarget = i

            # if ptarget >= 0:
            #     pqty = self.qty[ptarget]  # self.ids.qty_inp.text
            #     self.ids.qty_inp.text = pqty  # self.qty[ptarget]
            #     expr = '%s\t\tx\d\t' % (pname)
            #     rexpr = pname+'\t\tx'+str(pqty)+'\t'
            #     nu_text = re.sub(expr, rexpr, prev_text)
            #     preview.text = nu_text + purchase_total
            # else:
            self.cart.append(pcode)
            self.qty.append(self.ids.qty_inp.text)  # 1
            nu_preview = '\n'.join(
                [prev_text, pname+'\tx'+pqty+'\t'+str(price.text), purchase_total])
            preview.text = nu_preview
            print(self.cart)
            print(self.qty)

            self.ids.disc_perc_inp.text = 'Hmm!'
            self.ids.qty_inp.text = str(pqty)
            self.ids.price_inp.text = str(price.text)
            self.ids.vat_inp.text = '15%'
            self.ids.total_inp.text = str(pprice)

        # target_stock = target_code['in_stock']
        # target_stock -= str(pqty)
        # print(target_stock)

    def sold(self):
        pcode = self.ids.code_inp.text
        target_code = self.stocks.find_one({'product_code': pcode})
        print(target_code['sold'])
        target_code['sold'] += int(self.ids.qty_inp.text)
        print(target_code['sold'])
        print(target_code)
        # content = self.ids.code_inp
        # content.clear_widgets()
        # self.ids.refresh


class OperatorApp(App):
    def build(self):
        return OperatorWindow()


if __name__ == "__main__":
    oa = OperatorApp()
    oa.run()
