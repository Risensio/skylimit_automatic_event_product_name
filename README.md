# Skylimit Automatic Event Product Name

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-purple.svg)](https://github.com/odoo/odoo/tree/18.0)

A simple and efficient Odoo addon that automatically sets ticket names to match product names in events and event templates, eliminating duplicate data entry and ensuring consistency.

**Author**: iSensio | **Website**: https://isensio.com

## Features

- ✅ **Automatic Naming**: Ticket names are automatically populated from product names
- ✅ **Event Support**: Works with regular event tickets (`event.event.ticket`)
- ✅ **Template Support**: Works with event template tickets (`event.type.ticket`)
- ✅ **Real-time Updates**: Uses `@api.onchange` for immediate UI feedback
- ✅ **Creation & Updates**: Handles both new ticket creation and existing ticket modifications
- ✅ **Non-intrusive**: Only sets name when not explicitly provided by user

## Installation

### Prerequisites

- Odoo 18.0
- `event` module (standard Odoo)
- `event_product` module (standard Odoo)
- `product` module (standard Odoo)

### Steps

1. **Download the addon**:
   ```bash
   cd /path/to/your/odoo/addons
   git clone https://github.com/yourusername/odoo_automatic_event_product_name.git
   ```

2. **Update addons list**:
   - Go to Apps menu in Odoo
   - Click "Update Apps List"

3. **Install the module**:
   - Search for "Skylimit Automatic Event Product Name"
   - Click Install

## Usage

### For Event Tickets

1. Go to **Events > Configuration > Events**
2. Create or edit an event
3. In the **Tickets** tab:
   - Select a product in the **Product** field
   - The **Name** field will automatically populate with the product name
   - Save the ticket

### For Event Template Tickets

1. Go to **Events > Configuration > Event Categories**
2. Create or edit an event category
3. In the **Tickets** tab:
   - Select a product in the **Product** field
   - The **Name** field will automatically populate with the product name
   - Save the ticket template

## Technical Details

### Models Extended

- `event.event.ticket` - Regular event tickets
- `event.type.ticket` - Event template tickets

### Methods Implemented

- `_onchange_product_id_set_name()` - Real-time name update when product changes
- `create()` - Automatic naming during ticket creation
- `write()` - Automatic naming during ticket updates

### Code Structure

```
odoo_automatic_event_product_name/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── event_event.py
└── README.md
```

## Configuration

No additional configuration is required. The addon works automatically once installed.

## Compatibility

- **Odoo Version**: 18.0
- **Python**: 3.8+
- **Dependencies**: Standard Odoo modules only

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the LGPL v3 License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please create an issue on the [GitHub repository](https://github.com/yourusername/odoo_automatic_event_product_name/issues).

## Changelog

### Version 18.0.1.0.0
- Initial release
- Support for event tickets automatic naming
- Support for event template tickets automatic naming
- Real-time UI updates with onchange methods