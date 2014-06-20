/**
 * 	Author: Entpy software <developer at entpy dot com>
 * 	Version: 0.1.0
 *
 * 	License: GPL_v3 {Link: http://gplv3.fsf.org/}
 *
 *	Permission is hereby granted, free of charge, to any person obtaining
 *	a copy of this software and associated documentation files (the
 *	"Software"), to deal in the Software without restriction, including
 *	without limitation the rights to use, copy, modify, merge, publish,
 *	distribute, sublicense, and/or sell copies of the Software, and to
 *	permit persons to whom the Software is furnished to do so, subject to
 *	the following conditions:
 *
 *	The above copyright notice and this permission notice shall be
 *	included in all copies or substantial portions of the Software.
 *
 *	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 *	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 *      NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 *      LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 *      OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 *      WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

var FormValidatorClass = {

	/**
	 *  Flag to show error message
	 */
	showErrorMessages : false, // boolean true/false

	/**
	 * cleanWrongElement 
	 *
	 * Function to remove error class to an element
	 * 
	 * @access public
	 * @return void
	 */
	cleanWrongElement : function(wrongElement){
		if(this.showErrorMessages) {
			$(wrongElement).next(".validator_msg").remove();
		}
		$(wrongElement).removeClass("validator_error");

		return true;
	},

	/**
	 * validateFormData 
	 *
	 * Function to retrieve all element to check
	 * 
	 * @access public
	 * @return void
	 */
	validateFormData : function(){
		var returnVar = true;

		$(".elementToCheck").each(function(i) {
			if (!this.dataValidator($(this).data("value").split(" "), $(this))){
				returnVar = false;
			}
		});

		return returnVar;
	},

	/**
	 * dataValidator 
	 *
	 * Function to validate an element with a check
	 * 
	 * @param checkName $checkName 
	 * @param elementToCheck $elementToCheck 
	 * @access public
	 * @return void
	 */
	dataValidator : function(checkName, elementToCheck){
		var returnVar = true;

		if (checkName[0] && $(elementToCheck)) {

			// remove old error class
			this.cleanWrongElement(elementToCheck);

			for(var cont = 0; cont < checkName.length; cont++){
				var regex = false;
				regex = this.getValidatorRegexCheck(checkName[cont], "regex");
				if (regex) {
					if (!$(elementToCheck).val().match(regex)){
						// error: add class error
						$(elementToCheck).addClass("validator_error");
						if(this.showErrorMessages) {
							$(elementToCheck).after('<span class="validator_msg">' + this.getValidatorRegexCheck(checkName[cont], "errorMsg") + "</span>");
						}

						returnVar = false;
						break;
					}
				}
			}
		}

		return returnVar;
	},

	/**
	 * getValidatorRegexCheck 
	 *
	 * Function to retrieve a check:
	 * storeCheck // alphaCheck // alphaCheck // vatNumberCheck // taxCodeCheck // capCheck // phoneCheck // phoneCheck // emailCheck 
	 * use formValidatorMsg to overwrite default error messages
	 * 
	 * @param checkName $checkName 
	 * @access public
	 * @return void
	 */
	getValidatorRegexCheck : function(checkName, methodAttrName) {
		var regexList = Array();
		var valueRequested = false;

		try {
			var regexList = {
				storeCheck : {
					regex : /^(?:[A-Za-z0-9-\ ]+)?$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.storeCheck.errorMsg : "Please insert a valid store name")
				},
				alphaCheck : {
					regex : /^(?:[a-zA-Z\ ]+)?$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.alphaCheck.errorMsg : "Please insert only alphabetic characters")
				},
				vatNumberCheck : {
					regex : /^(?:[0-9]{11})?$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.vatNumberCheck.errorMsg : "Please check your VAT number")
				},
				taxCodeCheck : {
					regex : /^(?:[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1})?$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.taxCodeCheck.errorMsg : "Please check your tax code")
				},
				capCheck : {
					regex : /^(?:[0-9]{5})?$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.capCheck.errorMsg : "Please check your CAP")
				},
				phoneCheck : {
					regex : /^(?:(\+?[0-9]+)?)?$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.phoneCheck.errorMsg : "Please insert a valid phone number")
				},
				emailCheck : {
					regex : /^(?:[A-Za-z.]+[A-Za-z0-9-_.]*@[A-Za-z0-9-]+\.[.A-Za-z0-9-]+)?$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.emailCheck.errorMsg : "Please insert a valid email")
				},
				mandatoryCheck : {
					regex : /^.+$/,
					errorMsg : (typeof formValidatorMsg !== 'undefined' ? formValidatorMsg.mandatoryCheck.errorMsg : "This field is required")
				}
			};
		} catch(e) {
			// throw new exception
			console.log(e);
		}

		if (checkName && methodAttrName) {
			valueRequested = regexList[checkName][methodAttrName];
		}

		return valueRequested
	},

	/**
	 * objectIsDefined 
	 *
	 * Function to check if an object exists
	 * 
	 * @access public
	 * @return void
	 */
	objectIsDefined : function(objectToCheck) {
		var returnVar = false;

		if (typeof objectToCheck !== 'undefined') {
			returnVar = true;
		}

		return returnVar;
	}
};
